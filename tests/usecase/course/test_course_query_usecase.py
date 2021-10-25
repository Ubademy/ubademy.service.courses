from unittest.mock import MagicMock, Mock

import pytest

from app.domain.course import CourseNotFoundError
from app.infrastructure.sqlite.course import CourseQueryServiceImpl
from app.usecase.course import CourseQueryUseCaseImpl, CourseReadModel


class TestBookQueryUseCase:
    def test_fetch_course_by_id_should_return_course(self):

        session = MagicMock()
        course_query_service = CourseQueryServiceImpl(session)
        course_query_service.find_by_id = Mock(
            return_value=CourseReadModel(
                id="course_1",
                creator_id="creator_1",
                name="C Programming For Beginners - Master the C Language",
                price=10,
                language="English",
                description="This is a course",
                categories=["Programing"],
                created_at=1614007224642,
                updated_at=1614007224642,
            )
        )

        course_query_usecase = CourseQueryUseCaseImpl(course_query_service)

        book = course_query_usecase.fetch_course_by_id("course_1")

        assert book.name == "C Programming For Beginners - Master the C Language"

    def test_fetch_course_by_id_should_throw_course_not_found_error(self):

        session = MagicMock()
        course_query_service = CourseQueryServiceImpl(session)
        course_query_service.find_by_id = Mock(side_effect=CourseNotFoundError)

        course_query_usecase = CourseQueryUseCaseImpl(course_query_service)

        with pytest.raises(CourseNotFoundError):
            course_query_usecase.fetch_course_by_id("cPqw4yPVUM3fA9sqzpZmkL")

    def test_fetch_courses_should_return_courses(self):
        session = MagicMock()
        course_query_service = CourseQueryServiceImpl(session)
        course_query_service.find_all = Mock(
            return_value=[
                CourseReadModel(
                    id="course_1",
                    creator_id="creator_1",
                    name="C Programming For Beginners - Master the C Language",
                    price=10,
                    language="English",
                    description="This is a course",
                    categories=[],
                    created_at=1614007224642,
                    updated_at=1614007224642,
                ),
                CourseReadModel(
                    id="course_2",
                    creator_id="creator_2",
                    name="Learn Python Programming Masterclass",
                    price=20,
                    language="English",
                    description="This is a course",
                    categories=[],
                    created_at=1614007224642,
                    updated_at=1614007224642,
                ),
            ]
        )

        course_query_usecase = CourseQueryUseCaseImpl(course_query_service)
        courses = course_query_usecase.fetch_courses()

        assert len(courses) == 2
        assert courses[0].price == 10
        assert courses[1].price == 20
