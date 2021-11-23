from pydantic import BaseModel, Field

from app.domain.collab.collab_exception import (
    NoCollabsInCourseError,
    UserAlreadyInCourseError,
)


class ErrorMessageNoCollabsInCourse(BaseModel):
    detail: str = Field(example=NoCollabsInCourseError.message)


class ErrorMessageUserAlreadyInCourse(BaseModel):
    detail: str = Field(example=UserAlreadyInCourseError.message)
