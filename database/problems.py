from enum import Enum

from sqlalchemy import UUID
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey, Integer, String, event
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base_model import (
    Base,
    CreatedBaseModel,
    IDBaseModel,
    SlugBaseModel,
)


class TagProblem(Base):
    __tablename__ = "tag_problem"
    problem_id = mapped_column(ForeignKey("problems.id"), primary_key=True)
    tag_id = mapped_column(ForeignKey("tags.id"), primary_key=True)


class Tag(IDBaseModel, SlugBaseModel):
    name: Mapped[str] = mapped_column(String(255))

    problems: Mapped[list["Problem"]] = relationship(
        "Problem", secondary="tag_problem", back_populates="tags"
    )


class Problem(IDBaseModel, CreatedBaseModel, SlugBaseModel):
    class Difficulty(str, Enum):
        EASY = "easy"
        MEDIUM = "medium"
        HARD = "hard"

    tags: Mapped[list["Tag"]] = relationship(
        "Tag", secondary="tag_problem", back_populates="problems"
    )

    name: Mapped[str] = mapped_column(String(255))

    difficulty: Mapped[Difficulty] = mapped_column(
        SqlEnum(Difficulty, name="difficulty_enum"),
        nullable=False,
        default=Difficulty.EASY,
    )
    description: Mapped[str] = mapped_column(String)
    examples: Mapped[list["Example"]] = relationship(
        "Example", back_populates="problem"
    )


event.listen(Problem.name, "set", Problem.make_slug, retval=False)
event.listen(Tag.name, "set", Tag.make_slug, retval=False)


class Example(IDBaseModel):
    order_number: Mapped[int] = mapped_column(Integer, server_default="1")

    input: Mapped[str] = mapped_column(String)
    output: Mapped[str] = mapped_column(String)
    explanation: Mapped[str] = mapped_column(String)
    problem_id: Mapped[UUID] = mapped_column(
        ForeignKey("problems.id", ondelete="CASCADE")
    )
    problem: Mapped["Problem"] = relationship(
        "Problem", back_populates="examples"
    )
