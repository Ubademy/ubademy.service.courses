from unittest.mock import MagicMock, Mock

from app.domain.course import Course, CourseNotFoundError
from app.infrastructure.course import CourseDTO
from app.infrastructure.course.course_dto import Category, User

from app.usecase.course import CourseUpdateModel

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

course_1_update = CourseUpdateModel(
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

colab_1 = User(
    id="colab_1",
    user_id="colab_1",
    course_id="no_students",
    role="colab",
    active=True,
)

colab_2 = User(
    id="colab_2",
    user_id="colab_2",
    course_id="no_students",
    role="colab",
    active=True,
)

course_dto_no_students = CourseDTO(
    id="course_2",
    creator_id="creator_2",
    name="Learn Python Programming Masterclass",
    price=20,
    language="English",
    description="This is a course",
    categories=[],
    created_at=1614007224642,
    updated_at=1614007224642,
    users=[colab_1, colab_2],
)

student_1 = User(
    id="student_1",
    user_id="student_1",
    course_id="no_colabs",
    role="student",
    active=True,
)

student_2 = User(
    id="student_2",
    user_id="student_2",
    course_id="no_colabs",
    role="student",
    active=True,
)

course_dto_no_colabs = CourseDTO(
    id="course_3",
    creator_id="creator_2",
    name="Learn Python Programming Masterclass",
    price=20,
    language="English",
    description="This is a course",
    categories=[],
    created_at=1614007224642,
    updated_at=1614007224642,
    users=[student_1, student_2],
)


query_course_1 = MagicMock()
query_course_1.one = Mock(return_value=course_dto_1)
query_course_1.first = Mock(return_value=course_dto_1)

user_1 = User(
    id="user_0",
    user_id="user_0",
    course_id="course_1",
    role="student",
)


def mock_filter_course_1(id):
    if id == course_dto_1.id:
        return query_course_1
    raise CourseNotFoundError


def mock_filter_course_1_with_user(id=None, course_id=None, user_id=None):
    if id == course_dto_1.id or course_id == course_dto_1.id:
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


def mock_filter_course_no_students():
    return course_dto_no_students
