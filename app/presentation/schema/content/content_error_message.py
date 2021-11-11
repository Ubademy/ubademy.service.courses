from pydantic import BaseModel, Field

from app.domain.content.content_exception import ChapterAlreadyInCourseError


class ErrorMessageChapterAlreadyInCourse(BaseModel):
    detail: str = Field(example=ChapterAlreadyInCourseError.message)
