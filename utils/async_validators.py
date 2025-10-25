from fastapi import HTTPException

from database import Problem, User
from schemas import RegisterSchema
from schemas.problems import ProblemCreateSchema
from schemas.users import LoginSchema
from utils.functions import is_email
from utils.security import verify_password

from starlette import status

async def validate_email_and_username(data: RegisterSchema):
    if await User.exists(User.email == data.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    if await User.exists(User.username == data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered"
        )

    return data


async def check_username_and_password(data: LoginSchema):  # TODO
    if is_email(data.login):
        if not await User.exists(User.email == data.login):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email not found")
        else:
            user = await User.get(User.email == data.login)
    else:
        if not await User.exists(User.username == data.login):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username not found")
        else:
            user = await User.get(User.username == data.login)

    print(user.username, verify_password(data.password, user.password))

    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")

    return data


async def check_unique_constraint_to_problem(data: ProblemCreateSchema):
    print(data.name)
    print(Problem.exists(Problem.name == data.name))

    if await Problem.exists(Problem.name == data.name):
        raise HTTPException(status_code=status.HTTP_status.HTTP_400_BAD_REQUEST_BAD_REQUEST, detail="Problem already exists")

    return data
