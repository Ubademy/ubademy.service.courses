from unittest.mock import MagicMock, Mock

import pytest

from app.domain.course import CourseNameAlreadyExistsError
from app.infrastructure.course import (
    CourseCommandUseCaseUnitOfWorkImpl,
    CourseDTO,
    CourseRepositoryImpl,
)
from app.infrastructure.course.course_dto import Content
from app.usecase.course import CourseCommandUseCaseImpl
from tests.parameters import (
    content_1,
    content_1_update,
    course_1,
    course_1_update,
    mock_filter_course_1,
    mock_filter_course_1_content,
    mock_filter_course_1_name_course,
    mock_filter_course_1_reviewed,
    mock_filter_course_1_with_user,
    review_create_1,
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

    def test_delete_course_by_id(self):
        session = MagicMock()
        session.query(CourseDTO).filter_by = Mock(side_effect=mock_filter_course_1)
        course_repository = CourseRepositoryImpl(session)
        uow = CourseCommandUseCaseUnitOfWorkImpl(
            session=session, course_repository=course_repository
        )
        course_command_usecase = CourseCommandUseCaseImpl(uow=uow)

        course_command_usecase.delete_course_by_id(id=course_1.id)

        session.query(CourseDTO).filter_by.assert_called_with(id="course_1")

    def test_add_collab_should_return_collab(self):
        session = MagicMock()
        session.query(CourseDTO).filter_by = Mock(side_effect=mock_filter_course_1)
        course_repository = CourseRepositoryImpl(session)
        uow = CourseCommandUseCaseUnitOfWorkImpl(
            session=session, course_repository=course_repository
        )
        course_command_usecase = CourseCommandUseCaseImpl(uow=uow)

        user = course_command_usecase.add_collab(user_1.course_id, user_1.id)

        session.query(CourseDTO).filter_by.assert_called_with(id="course_1")
        assert user.id is user_1.id

    def test_deactivate_collab_from_course_should_deactivate_collab(self):
        session = MagicMock()
        session.query(CourseDTO).filter_by = Mock(
            side_effect=mock_filter_course_1_with_user
        )
        course_repository = CourseRepositoryImpl(session)
        uow = CourseCommandUseCaseUnitOfWorkImpl(
            session=session, course_repository=course_repository
        )
        course_command_usecase = CourseCommandUseCaseImpl(uow=uow)

        course_command_usecase.deactivate_collab_from_course(
            user_id="user_1", course_id="course_1"
        )

        session.query(CourseDTO).filter_by.assert_called_with(
            course_id="course_1", user_id="user_1"
        )

    def test_add_content_should_return_content(self):
        session = MagicMock()
        session.query(CourseDTO).filter_by = Mock(side_effect=mock_filter_course_1)
        course_repository = CourseRepositoryImpl(session)
        uow = CourseCommandUseCaseUnitOfWorkImpl(
            session=session, course_repository=course_repository
        )
        course_command_usecase = CourseCommandUseCaseImpl(uow=uow)

        content = course_command_usecase.add_content(content_1, "course_1")

        session.query(CourseDTO).filter_by.assert_called_with(id="course_1")
        assert content.chapter_title is content_1.chapter_title

    def test_update_content_should_return_updated_content(self):
        session = MagicMock()
        session.query(CourseDTO).filter_by = Mock(
            side_effect=mock_filter_course_1_content
        )
        course_repository = CourseRepositoryImpl(session)
        uow = CourseCommandUseCaseUnitOfWorkImpl(
            session=session, course_repository=course_repository
        )
        course_command_usecase = CourseCommandUseCaseImpl(uow=uow)

        content = course_command_usecase.update_content(
            course_id="course_1", data=content_1_update, content_id="content_1"
        )

        session.query(CourseDTO).filter_by.assert_called_with(id="course_1")
        assert content.chapter_title is "a"

    def test_add_review_should_return_review(self):
        session = MagicMock()
        session.query(CourseDTO).filter_by = Mock(
            side_effect=mock_filter_course_1_reviewed
        )
        course_repository = CourseRepositoryImpl(session)
        uow = CourseCommandUseCaseUnitOfWorkImpl(
            session=session, course_repository=course_repository
        )
        course_command_usecase = CourseCommandUseCaseImpl(uow=uow)

        review = course_command_usecase.add_review(id="course_1", data=review_create_1)

        session.query(CourseDTO).filter_by.assert_called_with(id="course_1")
        assert review.id is review_create_1.id
