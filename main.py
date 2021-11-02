import logging
from logging import config
from typing import Iterator, List, Optional

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm.session import Session

from app.domain.course import (
    CourseNameAlreadyExistsError,
    CourseNotFoundError,
    CourseRepository,
    CoursesNotFoundError,
)
from app.domain.user.user_exception import NoStudentsInCourseError, NoColabsInCourseError, NoUsersInCourseError
from app.infrastructure.sqlite.course import (
    CourseCommandUseCaseUnitOfWorkImpl,
    CourseQueryServiceImpl,
    CourseRepositoryImpl,
)
from app.infrastructure.sqlite.database import SessionLocal, create_tables
from app.presentation.schema.course.course_error_message import (
    ErrorMessageCourseNameAlreadyExists,
    ErrorMessageCourseNotFound,
    ErrorMessageCoursesNotFound,
)
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
from app.usecase.user.user_query_model import UserReadModel
from app.usecase.user.user_query_usecase import UserQueryUseCase, UserQueryUseCaseImpl

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


def user_query_usecase(session: Session = Depends(get_session)) -> UserQueryUseCase:
    course_query_service: CourseQueryService = CourseQueryServiceImpl(session)
    return UserQueryUseCaseImpl(course_query_service)


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
    data: CourseCreateModel,
    course_command_usecase: CourseCommandUseCase = Depends(course_command_usecase),
):
    try:
        course = course_command_usecase.create_course(data)
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
    response_model=List[CourseReadModel],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageCoursesNotFound,
        },
    },
    tags=["courses"],
)
async def get_courses(
    course_query_usecase: CourseQueryUseCase = Depends(course_query_usecase),
):
    try:
        courses = course_query_usecase.fetch_courses()

    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    if len(courses) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=CoursesNotFoundError.message,
        )

    return courses


@app.get(
    "/courses/",
    response_model=List[CourseReadModel],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageCoursesNotFound,
        },
    },
    tags=["courses"],
)
async def get_courses_filtering(
    name: Optional[str] = None,
    creator_id: Optional[str] = None,
    category: Optional[str] = None,
    ignore_free: Optional[bool] = None,
    ignore_paid: Optional[bool] = None,
    course_query_usecase: CourseQueryUseCase = Depends(course_query_usecase),
):
    try:
        courses = course_query_usecase.fetch_courses_by_filters(
            name=name,
            creator_id=creator_id,
            category=category,
            ignore_free=ignore_free,
            ignore_paid=ignore_paid,
        )

    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    if courses is None or len(courses) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=CoursesNotFoundError.message,
        )

    return courses


@app.get(
    "/courses/{course_id}",
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
    course_id: str,
    course_query_usecase: CourseQueryUseCase = Depends(course_query_usecase),
):
    try:
        course = course_query_usecase.fetch_course_by_id(course_id)

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


@app.get(
    "/courses/{course_id}/students",
    response_model=List[UserReadModel],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageCourseNotFound,
        },
    },
    tags=["users"],
)
async def get_course_students(
    course_id: str,
    user_query_usecase: UserQueryUseCase = Depends(user_query_usecase),
):
    try:
        students = user_query_usecase.fetch_students_by_id(course_id)

    except CourseNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except NoUsersInCourseError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except NoStudentsInCourseError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return students


@app.get(
    "/courses/{course_id}/colabs",
    response_model=List[UserReadModel],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageCourseNotFound,
        },
    },
    tags=["users"],
)
async def get_course_colabs(
    course_id: str,
    user_query_usecase: UserQueryUseCase = Depends(user_query_usecase),
):
    try:
        colabs = user_query_usecase.fetch_colabs_by_id(course_id)

    except CourseNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except NoUsersInCourseError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except NoColabsInCourseError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return colabs


@app.put(
    "/courses/{course_id}",
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
    course_id: str,
    data: CourseUpdateModel,
    course_command_usecase: CourseCommandUseCase = Depends(course_command_usecase),
):
    try:
        updated_course = course_command_usecase.update_course(course_id, data)
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

    return updated_course


@app.delete(
    "/courses/{course_id}",
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageCourseNotFound,
        },
    },
    tags=["courses"],
)
async def delete_course(
    course_id: str,
    course_command_usecase: CourseCommandUseCase = Depends(course_command_usecase),
):
    try:
        course_command_usecase.delete_course_by_id(course_id)
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
