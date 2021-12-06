import ast
import json
import logging
import os
from logging import config
from typing import Iterator, List, Optional

import requests
from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy.orm.session import Session
from starlette.requests import Request

from app.domain.collab.collab_exception import (
    NoCollabsInCourseError,
    UserAlreadyInCourseError,
    UserIsNotCreatorError,
)
from app.domain.content.content_exception import (
    ChapterAlreadyInCourseError,
    ContentNotFoundError,
)
from app.domain.course import (
    CourseNameAlreadyExistsError,
    CourseNotFoundError,
    CourseRepository,
    CoursesNotFoundError,
)
from app.domain.course.course_exception import CategoriesNotFoundError
from app.domain.review.review_exception import UserAlreadyReviewedCourseError
from app.infrastructure.course import (
    CourseCommandUseCaseUnitOfWorkImpl,
    CourseQueryServiceImpl,
    CourseRepositoryImpl,
)
from app.infrastructure.database import SessionLocal, create_tables
from app.presentation.schema.collab.collab_error_message import (
    ErrorMessageUserAlreadyInCourse,
)
from app.presentation.schema.content.content_error_message import (
    ErrorMessageChapterAlreadyInCourse,
)
from app.presentation.schema.course.course_error_message import (
    ErrorMessageCourseNameAlreadyExists,
    ErrorMessageCourseNotFound,
)
from app.presentation.schema.review.review_error_message import (
    ErrorMessageUserAlreadyReviewedCourse,
)
from app.usecase.collab.collab_query_model import (
    CollabReadModel,
    PaginatedUserReadModel,
)
from app.usecase.collab.collab_query_usecase import (
    CollabQueryUseCase,
    CollabQueryUseCaseImpl,
)
from app.usecase.content.content_command_model import (
    ContentCreateModel,
    ContentUpdateModel,
)
from app.usecase.content.content_query_model import ContentReadModel
from app.usecase.course import (
    CourseCommandUseCase,
    CourseCommandUseCaseImpl,
    CourseCommandUseCaseUnitOfWork,
    CourseCreateModel,
    CourseQueryService,
    CourseQueryUseCase,
    CourseQueryUseCaseImpl,
    CourseReadModel,
    CourseUpdateModel,
)
from app.usecase.course.course_query_model import PaginatedCourseReadModel
from app.usecase.review.review_command_model import ReviewCreateModel
from app.usecase.review.review_query_model import ReviewReadModel

config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)

app = FastAPI(title="courses")

create_tables()


def get_session() -> Iterator[Session]:
    session: Session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def course_query_usecase(session: Session = Depends(get_session)) -> CourseQueryUseCase:
    course_query_service: CourseQueryService = CourseQueryServiceImpl(session)
    return CourseQueryUseCaseImpl(course_query_service)


def user_query_usecase(session: Session = Depends(get_session)) -> CollabQueryUseCase:
    course_query_service: CourseQueryService = CourseQueryServiceImpl(session)
    return CollabQueryUseCaseImpl(course_query_service)


def course_command_usecase(
    session: Session = Depends(get_session),
) -> CourseCommandUseCase:
    course_repository: CourseRepository = CourseRepositoryImpl(session)
    uow: CourseCommandUseCaseUnitOfWork = CourseCommandUseCaseUnitOfWorkImpl(
        session, course_repository=course_repository
    )
    return CourseCommandUseCaseImpl(uow)


@app.post(
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
    course_command_usecase: CourseCommandUseCase = Depends(course_command_usecase),
):
    try:
        course = course_command_usecase.create_course(data, creator_id)
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


@app.get(
    "/courses",
    response_model=PaginatedCourseReadModel,
    status_code=status.HTTP_200_OK,
    tags=["courses"],
)
async def get_courses(
    limit: int = 50,
    offset: int = 0,
    course_query_usecase: CourseQueryUseCase = Depends(course_query_usecase),
):
    try:
        courses, count = course_query_usecase.fetch_courses(limit=limit, offset=offset)

    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    if len(courses) == 0:
        logger.info(CoursesNotFoundError.message)

    return PaginatedCourseReadModel(courses=courses, count=count)


@app.get(
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
    inactive: Optional[bool] = False,
    category: Optional[str] = None,
    language: Optional[str] = None,
    free: Optional[bool] = False,
    paid: Optional[bool] = False,
    text: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    course_query_usecase: CourseQueryUseCase = Depends(course_query_usecase),
):

    try:
        if not free and not paid:
            free = not free
            paid = not paid
        courses, count = course_query_usecase.fetch_courses_by_filters(
            ids=ids,
            name=name,
            creator_id=creator_id,
            collab_id=collab_id,
            subscription_id=subscription_id,
            inactive=inactive,
            category=category,
            language=language,
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


@app.get(
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
    course_query_usecase: CourseQueryUseCase = Depends(course_query_usecase),
):
    try:
        course = course_query_usecase.fetch_course_by_id(id)

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


def check_user_creator_permission(cid: str, uid: str, query: CourseQueryUseCase):
    if not query.user_is_creator(course_id=cid, user_id=uid):
        raise UserIsNotCreatorError


@app.patch(
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
    course_command_usecase: CourseCommandUseCase = Depends(course_command_usecase),
    query_usecase: CourseQueryUseCase = Depends(course_query_usecase),
):
    try:
        check_user_creator_permission(cid=id, uid=uid, query=query_usecase)  # type: ignore
        updated_course = course_command_usecase.update_course(id, data)
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


@app.delete(
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
    course_command_usecase: CourseCommandUseCase = Depends(course_command_usecase),
    query_usecase: CourseQueryUseCase = Depends(course_query_usecase),
):
    try:
        check_user_creator_permission(cid=id, uid=uid, query=query_usecase)  # type: ignore
        course_command_usecase.delete_course_by_id(id)
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


@app.post(
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


@app.get(
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


@app.post(
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
    course_command_usecase: CourseCommandUseCase = Depends(course_command_usecase),
    query_usecase: CourseQueryUseCase = Depends(course_query_usecase),
):
    try:
        check_user_creator_permission(cid=id, uid=uid, query=query_usecase)  # type: ignore
        collab = course_command_usecase.add_collab(course_id=id, user_id=user_id)
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


@app.patch(
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


try:
    microservices = os.environ["MICROSERVICES"]
    microservices = ast.literal_eval(microservices)
except KeyError as e:
    microservices = {}  # type: ignore


def get_users(uids, request, limit, offset):
    try:
        h = {"authorization": request.headers.get("authorization")}
        ids = ""
        for i in uids:
            ids = ids + i + ","
        logger.info(uids)
        return requests.get(
            microservices.get("users") + "users/filter-by-ids",
            headers=h,
            params={"ids": ids[:-1], "limit": limit, "offset": offset},
        )
    except:
        raise


@app.get(
    "/courses/{id}/collabs",
    response_model=PaginatedUserReadModel,
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
    user_query_usecase: CollabQueryUseCase = Depends(user_query_usecase),
):
    try:
        colabs = user_query_usecase.fetch_collabs_by_id(id)
        server_response = get_users(colabs, request, limit, offset)
        logger.info(server_response)
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


@app.get(
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


@app.post(
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


def check_user_involved_in_course(cid: str, uid: str, command: CourseCommandUseCase):
    if not command.user_involved(course_id=cid, user_id=uid):
        logger.info("User not creator")


@app.get(
    "/courses/{id}/content",
    response_model=List[ContentReadModel],
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


@app.patch(
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
