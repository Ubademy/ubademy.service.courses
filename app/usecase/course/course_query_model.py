from typing import cast

from pydantic import BaseModel, Field

from app.domain.course import Course


class CourseReadModel(BaseModel):

    id: str = Field(example="vytxeTZskVKR7C7WgdSP3d")
    name: str = Field(example="C Programming For Beginners - Master the C Language")
    categories: str = Field(example="Programming")
    price: int = Field(ge=0, example=10)
    created_at: int = Field(example=1136214245000)
    updated_at: int = Field(example=1136214245000)

    class Config:
        orm_mode = True

    @staticmethod
    def from_entity(course: Course) -> "CourseReadModel":
        return CourseReadModel(
            id=course.id,
            name=course.name,
            categories=course.categories,
            price=course.price,
            created_at=cast(int, course.created_at),
            updated_at=cast(int, course.updated_at),
        )
