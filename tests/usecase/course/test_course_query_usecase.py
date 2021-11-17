from unittest.mock import MagicMock, Mock

import pytest
from sqlalchemy.exc import NoResultFound

from app.domain.course import CourseNotFoundError, CoursesNotFoundError
from app.infrastructure.course import CourseDTO, CourseQueryServiceImpl
from app.usecase.course import CourseQueryUseCaseImpl
from tests.parameters import mock_fetch_all, mock_filter_course_1


class TestCourseQueryUseCase:
    def test_fetch_course_by_id_should_return_course(self):
        session = MagicMock()
        session.query(CourseDTO).filter_by = Mock(side_effect=mock_filter_course_1)
        course_query_service = CourseQueryServiceImpl(session)
        course_query_usecase = CourseQueryUseCaseImpl(course_query_service)

        book = course_query_usecase.fetch_course_by_id("course_1")

        session.query(CourseDTO).filter_by.assert_called_with(id="course_1")
        assert book.name == "C Programming For Beginners - Master the C Language"

    def test_fetch_course_by_id_should_throw_course_not_found_error(self):
        session = MagicMock()
        session.query(CourseDTO).filter_by = Mock(side_effect=CourseNotFoundError)
        course_query_service = CourseQueryServiceImpl(session)
        course_query_usecase = CourseQueryUseCaseImpl(course_query_service)

        with pytest.raises(CourseNotFoundError):
            course_query_usecase.fetch_course_by_id("cPqw4yPVUM3fA9sqzpZmkL")
        session.query(CourseDTO).filter_by.assert_called_with(
            id="cPqw4yPVUM3fA9sqzpZmkL"
        )

    def test_fetch_course_by_id_should_throw_no_result_found(self):
        session = MagicMock()
        session.query(CourseDTO).filter_by = Mock(side_effect=NoResultFound)
        course_query_service = CourseQueryServiceImpl(session)
        course_query_usecase = CourseQueryUseCaseImpl(course_query_service)

        with pytest.raises(CourseNotFoundError):
            course_query_usecase.fetch_course_by_id("cPqw4yPVUM3fA9sqzpZmkL")
        session.query(CourseDTO).filter_by.assert_called_with(
            id="cPqw4yPVUM3fA9sqzpZmkL"
        )

    def test_fetch_courses_should_return_courses(self):
        session = MagicMock()
        session.query(CourseDTO).order_by().slice().all = Mock(
            side_effect=mock_fetch_all
        )
        course_query_service = CourseQueryServiceImpl(session)
        course_query_usecase = CourseQueryUseCaseImpl(course_query_service)

        courses = course_query_usecase.fetch_courses()

        assert len(courses) == 2
        assert courses[0].price == 10
        assert courses[1].price == 20

    def test_fetch_courses_should_throw_courses_not_found_error(self):
        session = MagicMock()
        session.query(CourseDTO).order_by().slice().all = Mock(
            side_effect=CoursesNotFoundError
        )
        course_query_service = CourseQueryServiceImpl(session)
        course_query_usecase = CourseQueryUseCaseImpl(course_query_service)

        with pytest.raises(CoursesNotFoundError):
            course_query_usecase.fetch_courses()

    def test_fetch_courses_by_filters_with_no_filters_should_return_all(self):
        session = MagicMock()
        session.query(CourseDTO).slice().all = Mock(side_effect=mock_fetch_all)
        course_query_service = CourseQueryServiceImpl(session)
        course_query_usecase = CourseQueryUseCaseImpl(course_query_service)

        courses = course_query_usecase.fetch_courses_by_filters()

        assert len(courses) == 2
        assert courses[0].price == 10
        assert courses[1].price == 20
