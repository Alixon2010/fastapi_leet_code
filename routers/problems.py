from fastapi import APIRouter, Depends
from starlette import status

from database import Problem, Tag
from schemas.problems import ProblemCreateSchema, TagCreateSchema
from utils.async_validators import check_unique_constraint_to_problem
from utils.functions import (
    filter_by_tag,
    order_by_difficulty_,
    paginator,
    search_by_name_or_description,
)

problem_router = APIRouter()


@problem_router.get("/problems")
async def get_problems(
    page_size: int = 10,
    page_number: int = 1,
    search: str = None,
    order_by_difficulty: bool = False,
):
    problems = await Problem.all()
    if search is not None:
        problems = await search_by_name_or_description(search)

    if order_by_difficulty:
        problems = await order_by_difficulty_()

    problems = paginator(
        objects=problems, page_size=page_size, page_number=page_number
    )
    return {"message": f"problems in {page_number}-page", "data": problems}


@problem_router.get("/problems/{slug}")
async def get_problems_by_tag(
    slug, page_size: int = 10, page_number: int = 1, search: str = None
):
    problems = (await filter_by_tag(slug)).all()
    if search is not None:
        problems = await search_by_name_or_description(search)

    problems = paginator(
        objects=problems, page_size=page_size, page_number=page_number
    )
    return {"message": f"problems in {page_number}-page", "data": problems}


@problem_router.post("/problems")
async def create_problem(
    data: ProblemCreateSchema = Depends(check_unique_constraint_to_problem),
):
    print(data)
    problems = await Problem.create(**data.model_dump(exclude_none=True))
    return {"message": "problem created", "data": problems}


@problem_router.get("/tags")
async def get_all_tags():
    tags = await Tag.all()
    return {"tags": tags}


@problem_router.post("/tags", status_code=status.HTTP_201_CREATED)
async def create_tags(data: TagCreateSchema):
    await Tag.create(**data.model_dump(exclude_none=True, exclude_unset=True))
    return {"success": True}
