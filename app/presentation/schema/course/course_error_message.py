from pydantic import BaseModel, Field

from app.domain.course import (
    CourseNameAlreadyExistsError,
    CourseNotFoundError,
    CoursesNotFoundError,
)
from app.domain.course.course_exception import CategoriesNotFoundError


class ErrorMessageCourseNotFound(BaseModel):
    detail: str = Field(example=CourseNotFoundError.message)


class ErrorMessageCourseNameAlreadyExists(BaseModel):
    detail: str = Field(example=CourseNameAlreadyExistsError.message)


class ErrorMessageCoursesNotFound(BaseModel):
    detail: str = Field(example=CoursesNotFoundError.message)


class ErrorMessageCategoriesNotFound(BaseModel):
    detail: str = Field(example=CategoriesNotFoundError.message)
