import ast
import logging
import os
from typing import Iterator

import requests
from fastapi import Depends
from requests import Session

from app.domain.collab.collab_exception import UserIsNotCreatorError
from app.domain.course import CourseRepository
from app.infrastructure.course import (
    CourseCommandUseCaseUnitOfWorkImpl,
    CourseQueryServiceImpl,
    CourseRepositoryImpl,
)
from app.infrastructure.database import SessionLocal
from app.usecase.collab.collab_query_usecase import (
    CollabQueryUseCase,
    CollabQueryUseCaseImpl,
)
from app.usecase.course import (
    CourseCommandUseCase,
    CourseCommandUseCaseImpl,
    CourseCommandUseCaseUnitOfWork,
    CourseQueryService,
    CourseQueryUseCase,
    CourseQueryUseCaseImpl,
)

logger = logging.getLogger(__name__)


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


try:
    m: str = os.environ["MICROSERVICES"]
    microservices: dict = ast.literal_eval(m)
except KeyError as e:
    microservices = {}  # type: ignore


def get_users(uids, request, limit, offset):
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


def check_user_involved_in_course(cid: str, uid: str, command: CourseCommandUseCase):
    if not command.user_involved(course_id=cid, user_id=uid):
        logger.info("User not creator")


def check_user_creator_permission(cid: str, uid: str, query: CourseQueryUseCase):
    if not query.user_is_creator(course_id=cid, user_id=uid):
        raise UserIsNotCreatorError
