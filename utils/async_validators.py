from fastapi import HTTPException

from database import Problem, User
from schemas import RegisterSchema
from schemas.problems import ProblemCreateSchema
from schemas.users import LoginSchema
from utils.functions import is_email


async def validate_email_and_username(data: RegisterSchema):
    if await User.exists(User.email == data.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    if await User.exists(User.username == data.username):
        raise HTTPException(
            status_code=400, detail="Username already registered"
        )

    return data


async def check_username_and_password(data: LoginSchema):  # TODO
    if is_email(data.login):
        if not await User.exists(User.email == data.login):
            raise HTTPException(status_code=400, detail="Email not found")
    else:
        if not await User.exists(User.username == data.login):
            raise HTTPException(status_code=400, detail="Username not found")

    return data


async def check_unique_constraint_to_problem(data: ProblemCreateSchema):
    print(data.name)
    print(Problem.exists(Problem.name == data.name))

    if await Problem.exists(Problem.name == data.name):
        raise HTTPException(status_code=400, detail="Problem already exists")

    return data

