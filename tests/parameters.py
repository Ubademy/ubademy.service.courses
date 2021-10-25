from unittest.mock import MagicMock, Mock

from app.domain.course import Course, CourseNotFoundError
from app.infrastructure.sqlite.course import CourseDTO
from app.infrastructure.sqlite.course.course_dto import Category

course_dto_1 = CourseDTO(
    id="course_1",
    creator_id="creator_1",
    name="C Programming For Beginners - Master the C Language",
    price=10,
    language="English",
    description="This is a course",
    categories=[Category(category="Programing")],
    created_at=1614007224642,
    updated_at=1614007224642,
)

course_1 = Course(
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

course_dto_2 = CourseDTO(
    id="course_2",
    creator_id="creator_2",
    name="Learn Python Programming Masterclass",
    price=20,
    language="English",
    description="This is a course",
    categories=[],
    created_at=1614007224642,
    updated_at=1614007224642,
)

course_2 = CourseDTO(
    id="course_2",
    creator_id="creator_2",
    name="Learn Python Programming Masterclass",
    price=20,
    language="English",
    description="This is a course",
    categories=[],
    created_at=1614007224642,
    updated_at=1614007224642,
)


query_course_1 = MagicMock()
query_course_1.one = Mock(return_value=course_dto_1)


def mock_filter_course_1(id):
    if id == course_dto_1.id:
        return query_course_1
    raise CourseNotFoundError


def mock_filter_course_1_name(name):
    if name == course_dto_1.name:
        return query_course_1
    raise CourseNotFoundError


def mock_filter_course_1_name_course(name):
    if name == course_1.name:
        return course_1
    return None


def mock_filter_course_1_update(id=0, course_id=0):
    if id == course_dto_1.id or course_id == course_dto_1.id:
        return query_course_1
    raise CourseNotFoundError


def mock_fetch_all():
    return [course_dto_1, course_dto_2]
