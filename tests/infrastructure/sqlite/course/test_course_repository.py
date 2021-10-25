from unittest.mock import MagicMock, Mock

import pytest
from sqlalchemy.exc import NoResultFound

from app.domain.course import CourseNameAlreadyExistsError, CourseNotFoundError
from app.infrastructure.sqlite.course import CourseDTO, CourseRepositoryImpl
from tests.parameters import (
    course_1,
    mock_filter_course_1,
    mock_filter_course_1_name,
    mock_filter_course_1_update,
)


class TestCourseRepository:
    def test_find_by_id_should_return_course(self):
        session = MagicMock()
        session.query(CourseDTO).filter_by = Mock(side_effect=mock_filter_course_1)
        course_repository = CourseRepositoryImpl(session)

        book = course_repository.find_by_id("course_1")

        session.query(CourseDTO).filter_by.assert_called_with(id="course_1")
        assert book.name == "C Programming For Beginners - Master the C Language"

    def test_find_by_id_should_throw_course_not_found_error(self):
        session = MagicMock()
        session.query(CourseDTO).filter_by = Mock(side_effect=CourseNotFoundError)
        course_repository = CourseRepositoryImpl(session)

        with pytest.raises(CourseNotFoundError):
            course_repository.find_by_id("cPqw4yPVUM3fA9sqzpZmkL")
        session.query(CourseDTO).filter_by.assert_called_with(
            id="cPqw4yPVUM3fA9sqzpZmkL"
        )

    def test_find_by_id_should_throw_no_result_found(self):
        session = MagicMock()
        session.query(CourseDTO).filter_by = Mock(side_effect=NoResultFound)
        course_repository = CourseRepositoryImpl(session)

        courses = course_repository.find_by_id("cPqw4yPVUM3fA9sqzpZmkL")

        assert courses is None
        session.query(CourseDTO).filter_by.assert_called_with(
            id="cPqw4yPVUM3fA9sqzpZmkL"
        )

    def test_find_by_name_should_return_course(self):
        session = MagicMock()
        session.query(CourseDTO).filter_by = Mock(side_effect=mock_filter_course_1_name)
        course_repository = CourseRepositoryImpl(session)

        book = course_repository.find_by_name(
            "C Programming For Beginners - Master the C Language"
        )

        session.query(CourseDTO).filter_by.assert_called_with(
            name="C Programming For Beginners - Master the C Language"
        )
        assert book.name == "C Programming For Beginners - Master the C Language"

    def test_find_by_name_should_throw_course_not_found_error(self):
        session = MagicMock()
        session.query(CourseDTO).filter_by = Mock(side_effect=CourseNotFoundError)
        course_repository = CourseRepositoryImpl(session)

        with pytest.raises(CourseNotFoundError):
            course_repository.find_by_name("course_0")
        session.query(CourseDTO).filter_by.assert_called_with(name="course_0")

    def test_find_by_name_should_throw_no_result_found(self):
        session = MagicMock()
        session.query(CourseDTO).filter_by = Mock(side_effect=NoResultFound)
        course_repository = CourseRepositoryImpl(session)

        courses = course_repository.find_by_name("course_0")

        assert courses is None
        session.query(CourseDTO).filter_by.assert_called_with(name="course_0")

    def test_create_should_add_course_dto(self):
        session = MagicMock()
        session.add = Mock()
        course_repository = CourseRepositoryImpl(session)

        course_repository.create(course_1)

        session.add.assert_called_once()

    def test_create_should_throw_course_already_exists_error(self):
        session = MagicMock()
        session.add = Mock(side_effect=CourseNameAlreadyExistsError)
        course_repository = CourseRepositoryImpl(session)

        with pytest.raises(CourseNameAlreadyExistsError):
            course_repository.create(course_1)
        session.add.assert_called_once()

    def test_update_should_update_correct_course(self):
        session = MagicMock()
        session.query(CourseDTO).filter_by = Mock(
            side_effect=mock_filter_course_1_update
        )
        course_repository = CourseRepositoryImpl(session)

        course_repository.update(course_1)

        session.query(CourseDTO).filter_by.assert_called_with(course_id="course_1")

    def test_update_should_throw_course_not_found_error(self):
        session = MagicMock()
        session.query(CourseDTO).filter_by = Mock(side_effect=CourseNotFoundError)
        course_repository = CourseRepositoryImpl(session)

        with pytest.raises(CourseNotFoundError):
            course_repository.update(course_1)
        session.query(CourseDTO).filter_by.assert_called_with(id="course_1")

    def test_delete_by_id_should_delete_correct_course(self):
        session = MagicMock()
        session.query(CourseDTO).filter_by = Mock(side_effect=mock_filter_course_1)
        course_repository = CourseRepositoryImpl(session)

        course_repository.delete_by_id(id="course_1")

        session.query(CourseDTO).filter_by.assert_called_with(id="course_1")

    def test_delete_by_id_should_throw_course_not_found_error(self):
        session = MagicMock()
        session.query(CourseDTO).filter_by = Mock(side_effect=CourseNotFoundError)
        course_repository = CourseRepositoryImpl(session)

        with pytest.raises(CourseNotFoundError):
            course_repository.delete_by_id(id="course_1")
        session.query(CourseDTO).filter_by.assert_called_with(id="course_1")
