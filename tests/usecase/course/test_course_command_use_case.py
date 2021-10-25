from unittest.mock import MagicMock, Mock

import pytest

from app.domain.course import CourseNameAlreadyExistsError
from app.infrastructure.sqlite.course import CourseCommandUseCaseUnitOfWorkImpl
from app.usecase.course import CourseCommandUseCaseImpl
from tests.parameters import course_1, mock_filter_course_1_name_course


class TestCourseCommandUseCase:
    def test_create_course_should_return_course(self):
        session = MagicMock()
        course_repository = MagicMock()
        course_repository.find_by_name = Mock(return_value=None)
        course_repository.find_by_id = Mock(return_value=course_1)
        uow = CourseCommandUseCaseUnitOfWorkImpl(
            session=session, course_repository=course_repository
        )
        course_command_usecase = CourseCommandUseCaseImpl(uow=uow)

        course = course_command_usecase.create_course(course_1)

        assert course.name == course_1.name
        course_repository.find_by_name.assert_called_with(course_1.name)

    def test_create_course_when_course_exists_should_throw_course_name_already_exists_error(
        self,
    ):
        session = MagicMock()
        course_repository = MagicMock()
        course_repository.find_by_name = Mock(
            side_effect=mock_filter_course_1_name_course
        )
        course_repository.find_by_id = Mock(return_value=course_1)
        uow = CourseCommandUseCaseUnitOfWorkImpl(
            session=session, course_repository=course_repository
        )
        course_command_usecase = CourseCommandUseCaseImpl(uow=uow)

        with pytest.raises(CourseNameAlreadyExistsError):
            course_command_usecase.create_course(course_1)
        course_repository.find_by_name.assert_called_with(course_1.name)
