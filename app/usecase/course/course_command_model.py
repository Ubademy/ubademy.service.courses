from pydantic import BaseModel, Field


class CourseCreateModel(BaseModel):

    name: str = Field(example="C Programming For Beginners - Master the C Language")
    categories: str = Field(example="Programming")
    price: int = Field(ge=0, example=10)


class CourseUpdateModel(BaseModel):

    name: str = Field(example="C Programming For Beginners - Master the C Language")
    categories: str = Field(example="Programming")
    price: int = Field(ge=0, example=10)
