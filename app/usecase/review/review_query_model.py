from pydantic import BaseModel, Field


class ReviewReadModel(BaseModel):

    id: str = Field(example="vytxeTZskVKR7C7WgdSP3d")
    course_id: str = Field(example="TZskVKR")
    recommended: bool = Field(example=True)
    review: str = Field(
        example="Very engaging and teaches the course in a manner that's very easy to pick up. It "
        "doesnt matter if some lectures are beginner level lectures or more advanced "
        "programming concepts."
    )
    date: int = Field(example=1136214245000)
