from typing import List, cast

from pydantic import BaseModel, Field

from app.domain.course import Course


class CourseReadModel(BaseModel):

    id: str = Field(example="vytxeTZskVKR7C7WgdSP3d")
    creator_id: str = Field(example="creator1")
    name: str = Field(example="C Programming For Beginners - Master the C Language")
    price: int = Field(ge=0, example=10)
    language: str = Field(example="English")
    description: str = Field(example="Learn how to program with C")
    categories: List[str] = Field(example=["Programming"])
    created_at: int = Field(example=1136214245000)
    updated_at: int = Field(example=1136214245000)

    class Config:
        orm_mode = True

    @staticmethod
    def from_entity(course: Course) -> "CourseReadModel":
        return CourseReadModel(
            id=course.id,
            creator_id=course.creator_id,
            name=course.name,
            price=course.price,
            language=course.language,
            description=course.description,
            categories=course.categories,
            created_at=cast(int, course.created_at),
            updated_at=cast(int, course.updated_at),
        )
