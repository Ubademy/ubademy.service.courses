from typing import List

from pydantic import BaseModel, Field


class CourseCreateModel(BaseModel):

    name: str = Field(example="C Programming For Beginners - Master the C Language")
    price: float = Field(ge=0, example=10)
    language: str = Field(example="English")
    description: str = Field(example="Learn how to program with C")
    categories: List[str] = Field(example=["Programming"])
    video: str = Field(
        default="", example="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    )


class CourseUpdateModel(BaseModel):

    name: str = Field(
        default=None, example="C Programming For Beginners - Master the C Language"
    )
    price: float = Field(default=None, ge=0, example=10)
    language: str = Field(default=None, example="English")
    description: str = Field(default=None, example="Learn how to program with C")
    categories: List[str] = Field(default=None, example=["Programming"])
    video: str = Field(
        default=None, example="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    )
