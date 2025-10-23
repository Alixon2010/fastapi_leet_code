import re

from fastapi import HTTPException
from sqlalchemy import or_, select
from starlette import status

from database import Problem, Tag
from database.base_model import db


def is_email(value: str) -> bool:
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, value) is not None


def paginator(objects, page_size, page_number):
    if page_number * page_size - page_size > len(objects) - 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This page does not exist",
        )
    return objects[
        page_number * page_size - page_size: page_number * page_size
    ]


async def search_by_name_or_description(search):
    query = select(Problem).where(
        or_(
            Problem.name.ilike(f"{search}%"),
            Problem.description.ilike(f"{search}%"),
        )
    )
    return (await db.execute(query)).scalars().all()


async def filter_by_tag(slug: str):
    query = select(Problem).where(Problem.tags.any(Tag.slug == slug))
    result = await db.execute(query)
    return result.scalars()


async def order_by_difficulty_():
    from sqlalchemy import case, select

    difficulty_order = case(
        (Problem.difficulty == Problem.Difficulty.EASY, 1),
        (Problem.difficulty == Problem.Difficulty.MEDIUM, 2),
        (Problem.difficulty == Problem.Difficulty.HARD, 3),
    )

    problems = (
        (await db.execute(select(Problem).order_by(difficulty_order)))
        .scalars()
        .all()
    )
    return problems
