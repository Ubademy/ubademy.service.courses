from unittest.mock import MagicMock, Mock

import pytest

from app.domain.course import CourseNameAlreadyExistsError
from app.infrastructure.course import (
    CourseCommandUseCaseUnitOfWorkImpl,
    CourseDTO,
    CourseRepositoryImpl,
)
from app.usecase.course import CourseCommandUseCaseImpl
from tests.parameters import (
    course_1,
    course_1_update,
    mock_filter_course_1,
    mock_filter_course_1_name_course,
    mock_filter_course_1_with_user,
    user_1,
)


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

        course = course_command_usecase.create_course(course_1, course_1.creator_id)

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
            course_command_usecase.create_course(course_1, course_1.creator_id)
        course_repository.find_by_name.assert_called_with(course_1.name)

    def test_update_course_should_return_course(self):
        session = MagicMock()
        course_repository = MagicMock()
        course_repository.find_by_id = Mock(return_value=course_1)
        uow = CourseCommandUseCaseUnitOfWorkImpl(
            session=session, course_repository=course_repository
        )
        course_command_usecase = CourseCommandUseCaseImpl(uow=uow)

        course = course_command_usecase.update_course(
            id=course_1.id, data=course_1_update
        )

        assert course.name == course_1.name

    def test_add_user_should_return_user(self):
        session = MagicMock()
        session.query(CourseDTO).filter_by = Mock(side_effect=mock_filter_course_1)
        course_repository = CourseRepositoryImpl(session)
        uow = CourseCommandUseCaseUnitOfWorkImpl(
            session=session, course_repository=course_repository
        )
        course_command_usecase = CourseCommandUseCaseImpl(uow=uow)

        user = course_command_usecase.add_user(user_1, user_1.course_id)

        session.query(CourseDTO).filter_by.assert_called_with(id="course_1")
        assert user.id is user_1.id

    def test_deactivate_user_from_course_should_deactivate_user(self):
        session = MagicMock()
        session.query(CourseDTO).filter_by = Mock(
            side_effect=mock_filter_course_1_with_user
        )
        course_repository = CourseRepositoryImpl(session)
        uow = CourseCommandUseCaseUnitOfWorkImpl(
            session=session, course_repository=course_repository
        )
        course_command_usecase = CourseCommandUseCaseImpl(uow=uow)

        course_command_usecase.deactivate_user_from_course(
            user_id="user_1", course_id="course_1"
        )

        session.query(CourseDTO).filter_by.assert_called_with(
            course_id="course_1", user_id="user_1"
        )
