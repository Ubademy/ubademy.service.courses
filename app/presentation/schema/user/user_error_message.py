from pydantic import BaseModel, Field

from app.domain.user.user_exception import (
    NoColabsInCourseError,
    NoStudentsInCourseError,
    NoUsersInCourseError,
    UserAlreadyInCourseError,
)


class ErrorMessageNoUsersInCourse(BaseModel):
    detail: str = Field(example=NoUsersInCourseError.message)


class ErrorMessageNoColabsInCourse(BaseModel):
    detail: str = Field(example=NoColabsInCourseError.message)


class ErrorMessageNoStudentsInCourse(BaseModel):
    detail: str = Field(example=NoStudentsInCourseError.message)


class ErrorMessageUserAlreadyInCourse(BaseModel):
    detail: str = Field(example=UserAlreadyInCourseError.message)
