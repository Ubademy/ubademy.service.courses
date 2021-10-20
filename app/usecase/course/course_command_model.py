from typing import List

from pydantic import BaseModel, Field


class CourseCreateModel(BaseModel):

    creator_id: str = Field(example="creator1")
    name: str = Field(example="C Programming For Beginners - Master the C Language")
    price: float = Field(ge=0, example=10)
    language: str = Field(example="English")
    description: str = Field(example="Learn how to program with C")
    categories: List[str] = Field(example=["Programming"])


class CourseUpdateModel(BaseModel):

    name: str = Field(example="C Programming For Beginners - Master the C Language")
    price: float = Field(ge=0, example=10)
    language: str = Field(example="English")
    description: str = Field(example="Learn how to program with C")
    categories: List[str] = Field(example=["Programming"])
