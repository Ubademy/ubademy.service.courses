from unittest.mock import MagicMock, Mock

import pytest

from app.domain.user.user_exception import (
    NoColabsInCourseError,
    NoStudentsInCourseError,
)
from app.infrastructure.sqlite.course import CourseDTO, CourseQueryServiceImpl
from app.usecase.user.user_query_usecase import UserQueryUseCaseImpl
from tests.parameters import course_dto_no_colabs, course_dto_no_students


class TestUserQueryUseCase:
    def test_fetch_students_by_id_should_throw_no_students_in_course_error(self):
        session = MagicMock()
        session.query(CourseDTO).filter_by().one = Mock(
            return_value=course_dto_no_students
        )
        course_query_service = CourseQueryServiceImpl(session)
        user_query_usecase = UserQueryUseCaseImpl(course_query_service)

        with pytest.raises(NoStudentsInCourseError):
            user_query_usecase.fetch_students_by_id("course_0")

    def test_fetch_colabs_by_id_should_throw_no_colabs_in_course_error(self):
        session = MagicMock()
        session.query(CourseDTO).filter_by().one = Mock(
            return_value=course_dto_no_colabs
        )
        course_query_service = CourseQueryServiceImpl(session)
        user_query_usecase = UserQueryUseCaseImpl(course_query_service)

        with pytest.raises(NoColabsInCourseError):
            user_query_usecase.fetch_colabs_by_id("course_0")
