import json
import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from starlette.requests import Request

from app.domain.collab.collab_exception import (
    NoCollabsInCourseError,
    UserAlreadyInCourseError,
    UserIsNotCreatorError,
)
from app.domain.course import CourseNotFoundError
from app.presentation.schema.collab.collab_error_message import (
    ErrorMessageUserAlreadyInCourse,
)
from app.presentation.schema.course.course_error_message import (
    ErrorMessageCourseNotFound,
)
from app.usecase.collab.collab_query_model import CollabReadModel, UserReadModel
from app.usecase.collab.collab_query_usecase import CollabQueryUseCase
from app.usecase.course import CourseCommandUseCase, CourseQueryUseCase

from .dependencies import (
    check_user_creator_permission,
    course_command_usecase,
    course_query_usecase,
    get_users,
    user_query_usecase,
)

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/courses/{id}",
    response_model=CollabReadModel,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {
            "model": ErrorMessageUserAlreadyInCourse,
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageCourseNotFound,
        },
    },
    tags=["collabs"],
)
async def add_collab(
    id: str,
    uid: str,
    user_id: str,
    command_usecase: CourseCommandUseCase = Depends(course_command_usecase),
    query_usecase: CourseQueryUseCase = Depends(course_query_usecase),
):
    try:
        check_user_creator_permission(cid=id, uid=uid, query=query_usecase)  # type: ignore
        collab = command_usecase.add_collab(course_id=id, user_id=user_id)
    except UserAlreadyInCourseError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )
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

    return collab


@router.patch(
    "/courses/{id}/collabs/{user_id}",
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageCourseNotFound,
        },
    },
    tags=["collabs"],
)
async def deactivate_collab(
    id: str,
    user_id: str,
    uid: str,
    course_command_usecase: CourseCommandUseCase = Depends(course_command_usecase),
    query_usecase: CourseQueryUseCase = Depends(course_query_usecase),
):
    try:
        if user_id != uid:
            check_user_creator_permission(cid=id, uid=uid, query=query_usecase)  # type: ignore
        course_command_usecase.deactivate_collab_from_course(user_id, id)
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


@router.get(
    "/courses/{id}/collabs",
    response_model=List[UserReadModel],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageCourseNotFound,
        },
    },
    tags=["collabs"],
)
async def get_course_collabs(
    id: str,
    request: Request,
    limit: int = 50,
    offset: int = 0,
    query_usecase: CollabQueryUseCase = Depends(user_query_usecase),
):
    try:
        collabs = query_usecase.fetch_collabs_by_id(id)
        server_response = get_users(collabs, request, limit, offset)

    except NoCollabsInCourseError as e:
        logger.info(e)
        return []
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

    return json.loads(server_response.text)
