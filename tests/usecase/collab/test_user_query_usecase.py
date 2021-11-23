from unittest.mock import MagicMock, Mock

import pytest

from app.domain.collab.collab_exception import NoCollabsInCourseError
from app.infrastructure.course import CourseDTO, CourseQueryServiceImpl
from app.usecase.collab.collab_query_usecase import CollabQueryUseCaseImpl
from tests.parameters import course_dto_no_colabs


class TestUserQueryUseCase:
    def test_fetch_colabs_by_id_should_throw_no_collabs_in_course_error(self):
        session = MagicMock()
        session.query(CourseDTO).filter_by().first = Mock(
            return_value=course_dto_no_colabs
        )
        course_query_service = CourseQueryServiceImpl(session)
        user_query_usecase = CollabQueryUseCaseImpl(course_query_service)

        with pytest.raises(NoCollabsInCourseError):
            user_query_usecase.fetch_collabs_by_id("course_0")
