from pydantic import BaseModel, Field

from app.domain.review.review_exception import UserAlreadyReviewedCourseError


class ErrorMessageUserAlreadyReviewedCourse(BaseModel):
    detail: str = Field(example=UserAlreadyReviewedCourseError.message)
