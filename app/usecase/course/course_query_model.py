from typing import List, cast

from pydantic import BaseModel, Field

from app.domain.course import Course


class CourseReadModel(BaseModel):

    id: str = Field(example="vytxeTZskVKR7C7WgdSP3d")
    creator_id: str = Field(example="creator1")
    name: str = Field(example="C Programming For Beginners - Master the C Language")
    price: float = Field(ge=0, example=10)
    active: bool = Field(example=True)
    subscription_id: int = Field(ge=0, le=2, example=0)
    language: str = Field(example="English")
    country: str = Field(example="Argentina")
    description: str = Field(example="Learn how to program with C")
    categories: List[str] = Field(example=["Programming", "C"])
    recommendations: dict = Field(example={"recommended": 386, "total": 410})
    presentation_video: str = Field(
        example="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    )
    image: str = Field(
        example="https://static01.nyt.com/images/2017/09/26/science/26TB-PANDA/26TB-PANDA-superJumbo.jpg"
    )
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
            active=course.active,
            subscription_id=course.subscription_id,
            recommendations=course.recommendations,
            language=course.language,
            country=course.country,
            description=course.description,
            categories=course.categories,
            presentation_video=course.presentation_video,
            image=course.image,
            created_at=cast(int, course.created_at),
            updated_at=cast(int, course.updated_at),
        )


class PaginatedCourseReadModel(BaseModel):
    courses: List[CourseReadModel] = Field(example=CourseReadModel.schema())
    count: int = Field(ge=0, example=1)
