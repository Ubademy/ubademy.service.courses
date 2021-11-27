from pydantic import BaseModel, Field


class ReviewCreateModel(BaseModel):

    id: str = Field(example="vytxeTZskVKR7C7WgdSP3d")
    recommended: bool = Field(example=True)
    review: str = Field(
        example="Very engaging and teaches the course in a manner that's very easy to pick up. It "
        "doesnt matter if some lectures are beginner level lectures or more advanced "
        "programming concepts.",
        default="",
    )
