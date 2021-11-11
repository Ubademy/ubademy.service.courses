from pydantic import Field, BaseModel

from app.domain.user.content.content_exception import ChapterAlreadyInCourseError


class ErrorMessageChapterAlreadyInCourse(BaseModel):
    detail: str = Field(example=ChapterAlreadyInCourseError.message)
