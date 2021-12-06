from unittest.mock import MagicMock, Mock

from app.domain.course import Course, CourseNotFoundError
from app.infrastructure.course import CourseDTO
from app.infrastructure.course.course_dto import Category, Collab, Content
from app.usecase.content.content_command_model import (
    ContentCreateModel,
    ContentUpdateModel,
)
from app.usecase.course import CourseUpdateModel
from app.usecase.review.review_command_model import ReviewCreateModel

content_1 = ContentCreateModel(
    chapter_title="FFT: Fast Fourier Transform",
    subtitle="Definition",
    chapter=2,
    order=0,
    description="A fast Fourier transform (FFT) is an algorithm.",
    video="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    image="https://static01.nyt.com/images/2017/09/26/science/26TB-PANDA/26TB-PANDA-superJumbo.jpg",
)

content_1_update = ContentUpdateModel(
    chapter_title="a",
    chapter=3,
    order=0,
    description="b",
    video="c",
    image="d",
)

content_dto_1 = Content(
    id="content_1",
    chapter_title="FFT: Fast Fourier Transform",
    subtitle="Definition",
    chapter=1,
    order=0,
    description="A fast Fourier transform (FFT) is an algorithm.",
    video="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    image="https://static01.nyt.com/images/2017/09/26/science/26TB-PANDA/26TB-PANDA-superJumbo.jpg",
    active=True,
)

course_dto_1 = CourseDTO(
    id="course_1",
    creator_id="creator_1",
    name="C Programming For Beginners - Master the C Language",
    price=10,
    subscription_id=0,
    language="English",
    description="This is a course",
    categories=[Category(category="Programing")],
    presentation_video="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    image="https://static01.nyt.com/images/2017/09/26/science/26TB-PANDA/26TB-PANDA-superJumbo.jpg",
    content=[content_dto_1],
    reviews=[],
    created_at=1614007224642,
    updated_at=1614007224642,
)

course_dto_1_reviewed = CourseDTO(
    id="course_1",
    creator_id="creator_1",
    name="C Programming For Beginners - Master the C Language",
    price=10,
    subscription_id=0,
    language="English",
    description="This is a course",
    categories=[Category(category="Programing")],
    presentation_video="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    image="https://static01.nyt.com/images/2017/09/26/science/26TB-PANDA/26TB-PANDA-superJumbo.jpg",
    content=[content_dto_1],
    reviews=[],
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
    presentation_video="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    image="https://static01.nyt.com/images/2017/09/26/science/26TB-PANDA/26TB-PANDA-superJumbo.jpg",
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
    recommendations={},
    presentation_video="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    image="https://static01.nyt.com/images/2017/09/26/science/26TB-PANDA/26TB-PANDA-superJumbo.jpg",
    subscription_id=0,
    created_at=1614007224642,
    updated_at=1614007224642,
)

course_dto_2 = CourseDTO(
    id="course_2",
    creator_id="creator_2",
    name="Learn Python Programming Masterclass",
    price=20,
    subscription_id=0,
    language="English",
    description="This is a course",
    categories=[],
    reviews=[],
    presentation_video="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    image="https://static01.nyt.com/images/2017/09/26/science/26TB-PANDA/26TB-PANDA-superJumbo.jpg",
    created_at=1614007224642,
    updated_at=1614007224642,
)

course_2 = CourseDTO(
    id="course_2",
    creator_id="creator_2",
    name="Learn Python Programming Masterclass",
    price=20,
    subscription_id=0,
    language="English",
    description="This is a course",
    categories=[],
    presentation_video="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    image="https://static01.nyt.com/images/2017/09/26/science/26TB-PANDA/26TB-PANDA-superJumbo.jpg",
    created_at=1614007224642,
    updated_at=1614007224642,
    reviews=[],
)

colab_1 = Collab(
    id="colab_1",
    user_id="colab_1",
    course_id="no_students",
    active=True,
)

colab_2 = Collab(
    id="colab_2",
    user_id="colab_2",
    course_id="no_students",
    active=True,
)

course_dto_no_colabs = CourseDTO(
    id="course_3",
    creator_id="creator_2",
    name="Learn Python Programming Masterclass",
    price=20,
    subscription_id=0,
    language="English",
    description="This is a course",
    categories=[],
    presentation_video="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    image="https://static01.nyt.com/images/2017/09/26/science/26TB-PANDA/26TB-PANDA-superJumbo.jpg",
    created_at=1614007224642,
    updated_at=1614007224642,
    collabs=[],
    reviews=[],
)

review_create_1 = ReviewCreateModel(
    id="user_1",
    recommended=True,
    review="Hola",
)


query_course_1 = MagicMock()
query_course_1.one = Mock(return_value=course_dto_1)
query_course_1.first = Mock(return_value=course_dto_1)

query_course_1_reviewed = MagicMock()
query_course_1_reviewed.one = Mock(return_value=course_dto_1_reviewed)
query_course_1_reviewed.first = Mock(return_value=course_dto_1_reviewed)

query_content_1 = MagicMock()
query_content_1.one = Mock(return_value=content_dto_1)
query_content_1.first = Mock(return_value=content_dto_1)

user_1 = Collab(
    id="user_0",
    user_id="user_0",
    course_id="course_1",
    active=True,
)


def mock_filter_course_1_content(id):
    if id == course_dto_1.id:
        return query_course_1
    if id == content_dto_1.id:
        return query_content_1
    raise CourseNotFoundError


def mock_filter_course_1(id):
    if id == course_dto_1.id:
        return query_course_1
    raise CourseNotFoundError


def mock_filter_course_1_reviewed(id):
    if id == course_dto_1_reviewed.id:
        return query_course_1_reviewed
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
