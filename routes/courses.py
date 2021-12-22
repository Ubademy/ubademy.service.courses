import json
import logging
from typing import List, Optional

import requests
from fastapi import APIRouter, Depends, HTTPException, Query
from starlette import status

from app.domain.collab.collab_exception import UserIsNotCreatorError
from app.domain.course import (
    CourseNameAlreadyExistsError,
    CourseNotFoundError,
    CoursesNotFoundError,
)
from app.domain.course.course_exception import (
    CategoriesNotFoundError,
    NotEnoughFundsError,
)
from app.presentation.schema.course.course_error_message import (
    ErrorMessageCourseNameAlreadyExists,
    ErrorMessageCourseNotFound,
)
from app.usecase.course import (
    CourseCommandUseCase,
    CourseCreateModel,
    CourseQueryUseCase,
    CourseReadModel,
    CourseUpdateModel,
)
from app.usecase.course.course_query_model import PaginatedCourseReadModel

from .dependencies import (
    check_user_creator_permission,
    course_command_usecase,
    course_query_usecase,
    microservices,
)

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/courses",
    response_model=CourseReadModel,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {
            "model": ErrorMessageCourseNameAlreadyExists,
        },
    },
    tags=["courses"],
)
async def create_course(
    creator_id: str,
    data: CourseCreateModel,
    command_usecase: CourseCommandUseCase = Depends(course_command_usecase),
):
    try:
        course = command_usecase.create_course(data, creator_id)
    except CourseNameAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return course


@router.get(
    "/courses",
    response_model=PaginatedCourseReadModel,
    status_code=status.HTTP_200_OK,
    tags=["courses"],
)
async def get_courses(
    limit: int = 50,
    offset: int = 0,
    query_usecase: CourseQueryUseCase = Depends(course_query_usecase),
):
    try:
        courses, count = query_usecase.fetch_courses(limit=limit, offset=offset)

    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    if len(courses) == 0:
        logger.info(CoursesNotFoundError.message)

    return PaginatedCourseReadModel(courses=courses, count=count)


@router.get(
    "/courses/",
    response_model=PaginatedCourseReadModel,
    status_code=status.HTTP_200_OK,
    tags=["courses"],
)
async def get_courses_filtering(
    ids: Optional[List[str]] = Query(None),
    name: Optional[str] = None,
    creator_id: Optional[str] = None,
    collab_id: Optional[str] = None,
    subscription_id: Optional[int] = None,
    inactive_courses: Optional[bool] = False,
    inactive_collab: Optional[bool] = False,
    category: Optional[str] = None,
    language: Optional[str] = None,
    country: Optional[str] = None,
    free: Optional[bool] = False,
    paid: Optional[bool] = False,
    text: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    query_usecase: CourseQueryUseCase = Depends(course_query_usecase),
):
    try:
        if not free and not paid:
            free = not free
            paid = not paid
        courses, count = query_usecase.fetch_courses_by_filters(
            ids=ids,
            name=name,
            creator_id=creator_id,
            collab_id=collab_id,
            subscription_id=subscription_id,
            inactive_courses=inactive_courses,
            inactive_collab=inactive_collab,
            category=category,
            language=language,
            country=country,
            ignore_free=not free,
            ignore_paid=not paid,
            text=text,
            limit=limit,
            offset=offset,
        )

    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    if courses is None or len(courses) == 0:
        logger.info(CoursesNotFoundError.message)

    return PaginatedCourseReadModel(courses=courses, count=count)


@router.get(
    "/courses/{id}",
    response_model=CourseReadModel,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageCourseNotFound,
        },
    },
    tags=["courses"],
)
async def get_course(
    id: str,
    query_usecase: CourseQueryUseCase = Depends(course_query_usecase),
):
    try:
        course = query_usecase.fetch_course_by_id(id)

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

    return course


@router.patch(
    "/courses/{id}",
    response_model=CourseReadModel,
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageCourseNotFound,
        },
    },
    tags=["courses"],
)
async def update_course(
    id: str,
    uid: str,
    data: CourseUpdateModel,
    command_usecase: CourseCommandUseCase = Depends(course_command_usecase),
    query_usecase: CourseQueryUseCase = Depends(course_query_usecase),
):
    try:
        check_user_creator_permission(cid=id, uid=uid, query=query_usecase)  # type: ignore
        updated_course = command_usecase.update_course(id, data)
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

    return updated_course


def check_cancel_fee(c, id):
    url_subs: str = microservices.get("subscriptions")  # type: ignore
    url_payments: str = microservices.get("payments")  # type: ignore
    wallet = requests.get(url_payments + "payments/wallet/" + c.creator_id)
    cancel_fee = requests.get(
        url_subs + "subscriptions/" + id + "/enrollments/cancel-fee",
        params={"creator_id": c.creator_id, "price": c.price, "sub_id": c.subscription_id},  # type: ignore
    )
    logger.info(wallet.text)
    logger.info(cancel_fee.text)
    if float(json.loads(wallet.text)["balance"]) <= float(
            json.loads(cancel_fee.text)
    ):
        raise NotEnoughFundsError




@router.delete(
    "/courses/{id}",
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageCourseNotFound,
        },
    },
    tags=["courses"],
)
async def delete_course(
    id: str,
    uid: str,
    command_usecase: CourseCommandUseCase = Depends(course_command_usecase),
    query_usecase: CourseQueryUseCase = Depends(course_query_usecase),
):
    try:
        check_user_creator_permission(cid=id, uid=uid, query=query_usecase)  # type: ignore
        c = query_usecase.fetch_course_by_id(id)
        if c is None:
            raise CourseNotFoundError

        check_cancel_fee(c, id)

        url_subs: str = microservices.get("subscriptions")  # type: ignore
        requests.patch(
            url_subs + "subscriptions/" + id + "/enrollments",
            params={
                "course_name": c.name,
                "creator_id": c.creator_id,
                "price": c.price,
                "sub_id": c.subscription_id,
            },
        )

        command_usecase.delete_course_by_id(id)
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
    except NotEnoughFundsError as e:
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
    "/courses/categories/",
    response_model=List[str],
    status_code=status.HTTP_200_OK,
    tags=["courses"],
)
async def get_categories(
    course_query_usecase: CourseQueryUseCase = Depends(course_query_usecase),
):
    try:
        categories = course_query_usecase.fetch_categories()

    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    if len(categories) == 0:
        logger.info(CategoriesNotFoundError.message)

    return categories
