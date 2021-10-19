from pydantic import BaseModel, Field

from app.domain.course import (
    CourseNameAlreadyExistsError,
    CourseNotFoundError,
    CoursesNotFoundError,
)


class ErrorMessageCourseNotFound(BaseModel):
    detail: str = Field(example=CourseNotFoundError.message)


class ErrorMessageCourseNameAlreadyExists(BaseModel):
    detail: str = Field(example=CourseNameAlreadyExistsError.message)


class ErrorMessageCoursesNotFound(BaseModel):
    detail: str = Field(example=CoursesNotFoundError.message)
