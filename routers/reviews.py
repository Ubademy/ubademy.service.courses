import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.domain.course import CourseNotFoundError
from app.domain.review.review_exception import UserAlreadyReviewedCourseError
from app.presentation.schema.course.course_error_message import (
    ErrorMessageCourseNotFound,
)
from app.presentation.schema.review.review_error_message import (
    ErrorMessageUserAlreadyReviewedCourse,
)
from app.usecase.course import CourseCommandUseCase, CourseQueryUseCase
from app.usecase.review.review_command_model import ReviewCreateModel
from app.usecase.review.review_query_model import ReviewReadModel

from .dependencies import course_command_usecase, course_query_usecase

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/courses/{id}/reviews",
    response_model=ReviewReadModel,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {
            "model": ErrorMessageUserAlreadyReviewedCourse,
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageCourseNotFound,
        },
    },
    tags=["reviews"],
)
async def add_review(
    id: str,
    data: ReviewCreateModel,
    course_command_usecase: CourseCommandUseCase = Depends(course_command_usecase),
):
    try:
        review = course_command_usecase.add_review(id=id, data=data)
    except UserAlreadyReviewedCourseError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )
    except CourseNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return review


@router.get(
    "/courses/{id}/reviews",
    response_model=List[ReviewReadModel],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageCourseNotFound,
        },
    },
    tags=["reviews"],
)
async def get_reviews(
    id: str,
    query_usecase: CourseQueryUseCase = Depends(course_query_usecase),
):
    try:
        reviews = query_usecase.fetch_reviews_by_id(id)

    except CourseNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return reviews
