from fastapi import APIRouter, Depends, Response

from database import User
from schemas import RegisterSchema
from schemas.token import TokenSchema
from schemas.users import LoginSchema, UserOutSchema, UserUpdateSchema
from utils.async_validators import (
    check_username_and_password,
    validate_email_and_username,
)
from utils.security import (
    create_access_token,
    create_refresh_token,
    get_current_user,
)

user_router = APIRouter()


@user_router.get("/me", response_model=UserOutSchema)
async def get_me(user: User = Depends(get_current_user)):
    return UserOutSchema.model_validate(user, from_attributes=True)


@user_router.patch("/user_update", response_model=UserOutSchema)
async def all_users(data: UserUpdateSchema, user: User = Depends(get_current_user)):
    await user.update(user.id, **data.model_dump(exclude_none=True))
    return user


@user_router.post("/auth/register", tags=["auth"])
async def register_user(
    data: RegisterSchema = Depends(validate_email_and_username),
):
    await User.create(**data.model_dump(exclude_none=True))
    return {"message": "check your email"}


@user_router.post("/auth/login", tags=["auth"], response_model=TokenSchema)
async def login_user(
    response: Response,
    data: LoginSchema = Depends(check_username_and_password),
):
    access_token = create_access_token(data={"sub": data.login})
    refresh_token = create_refresh_token(data={"sub": data.login})

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
    )

    return TokenSchema(access_token=access_token)
