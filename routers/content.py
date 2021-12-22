import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.domain.collab.collab_exception import UserIsNotCreatorError
from app.domain.content.content_exception import (
    ChapterAlreadyInCourseError,
    ContentNotFoundError,
)
from app.domain.course import CourseNotFoundError
from app.presentation.schema.content.content_error_message import (
    ErrorMessageChapterAlreadyInCourse,
)
from app.presentation.schema.course.course_error_message import (
    ErrorMessageCourseNotFound,
)
from app.usecase.content.content_command_model import (
    ContentCreateModel,
    ContentUpdateModel,
)
from app.usecase.content.content_query_model import ChapterReadModel, ContentReadModel
from app.usecase.course import CourseCommandUseCase, CourseQueryUseCase

from .dependencies import (
    check_user_creator_permission,
    check_user_involved_in_course,
    course_command_usecase,
    course_query_usecase,
)

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post(
    "/courses/{id}/content",
    response_model=ContentReadModel,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageCourseNotFound,
        },
        status.HTTP_409_CONFLICT: {
            "model": ErrorMessageChapterAlreadyInCourse,
        },
    },
    tags=["content"],
)
async def add_content(
    data: ContentCreateModel,
    id: str,
    uid: str,
    course_command_usecase: CourseCommandUseCase = Depends(course_command_usecase),
    query_usecase: CourseQueryUseCase = Depends(course_query_usecase),
):
    try:
        check_user_creator_permission(cid=id, uid=uid, query=query_usecase)  # type: ignore
        content = course_command_usecase.add_content(data=data, course_id=id)
    except CourseNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except ChapterAlreadyInCourseError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )
    except UserIsNotCreatorError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=e.message,
        )
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return content


@router.get(
    "/courses/{id}/content",
    response_model=List[ChapterReadModel],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageCourseNotFound,
        },
    },
    tags=["content"],
)
async def get_content(
    id: str,
    uid: str,
    command_usecase: CourseCommandUseCase = Depends(course_command_usecase),
    query_usecase: CourseQueryUseCase = Depends(course_query_usecase),
):
    try:
        check_user_involved_in_course(cid=id, uid=uid, command=command_usecase)  # type: ignore
        content = query_usecase.fetch_content_by_id(id)

    except CourseNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except UserIsNotCreatorError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=e.message,
        )
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return content


@router.patch(
    "/courses/{id}/content/{content_id}",
    response_model=ContentReadModel,
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageCourseNotFound,
        },
        status.HTTP_409_CONFLICT: {
            "model": ErrorMessageChapterAlreadyInCourse,
        },
    },
    tags=["content"],
)
async def update_content(
    id: str,
    content_id: str,
    data: ContentUpdateModel,
    uid: str,
    course_command_usecase: CourseCommandUseCase = Depends(course_command_usecase),
    query_usecase: CourseQueryUseCase = Depends(course_query_usecase),
):
    try:
        check_user_creator_permission(cid=id, uid=uid, query=query_usecase)  # type: ignore
        updated_content = course_command_usecase.update_content(
            course_id=id, data=data, content_id=content_id
        )
    except CourseNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except ContentNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except ChapterAlreadyInCourseError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )

    except UserIsNotCreatorError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=e.message,
        )
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return updated_content
