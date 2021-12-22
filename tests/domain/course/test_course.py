import pytest

from app.domain.course import Course


class TestCourse:
    def test_constructor_should_create_instance(self):
        course = Course(
            id="course_1",
            creator_id="creator_1",
            name="C Programming For Beginners - Master the C Language",
            price=10,
            language="English",
            country="Argentina",
            description="This is a course",
            categories=["Programming"],
            presentation_video="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            image="https://static01.nyt.com/images/2017/09/26/science/26TB-PANDA/26TB-PANDA-superJumbo.jpg",
            subscription_id=0,
            recommendations={},
            active=True,
        )

        assert course.id == "course_1"
        assert course.creator_id == "creator_1"
        assert course.name == "C Programming For Beginners - Master the C Language"
        assert course.price == 10
        assert course.language == "English"
        assert course.description == "This is a course"
        assert course.categories == ["Programming"]

    def test_course_entity_should_be_identified_by_id(self):
        course_1 = Course(
            id="course_1",
            creator_id="creator_1",
            name="C Programming For Beginners - Master the C Language",
            price=10,
            language="English",
            country="Argentina",
            description="This is a course",
            categories=["Programming"],
            presentation_video="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            image="https://static01.nyt.com/images/2017/09/26/science/26TB-PANDA/26TB-PANDA-superJumbo.jpg",
            subscription_id=0,
            recommendations={},
            active=True,
        )

        course_2 = Course(
            id="course_1",
            creator_id="creator_1",
            name="Learn Python Programming Masterclass",
            price=20,
            language="English",
            country="Argentina",
            description="This is a course",
            categories=["Programming"],
            presentation_video="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            image="https://static01.nyt.com/images/2017/09/26/science/26TB-PANDA/26TB-PANDA-superJumbo.jpg",
            subscription_id=0,
            recommendations={},
            active=True,
        )

        course_3 = Course(
            id="course_3",
            creator_id="creator_1",
            name="C Programming For Beginners - Master the C Language",
            price=10,
            language="English",
            country="Argentina",
            description="This is a course",
            categories=["Programming"],
            presentation_video="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            image="https://static01.nyt.com/images/2017/09/26/science/26TB-PANDA/26TB-PANDA-superJumbo.jpg",
            subscription_id=0,
            recommendations={},
            active=True,
        )

        assert course_1 == course_2
        assert course_1 != course_3

    @pytest.mark.parametrize(
        "price",
        [
            (0),
            (1),
            (320),
        ],
    )
    def test_price_setter_should_update_value(self, price):
        course = Course(
            id="course_1",
            creator_id="creator_1",
            name="C Programming For Beginners - Master the C Language",
            price=10,
            language="English",
            country="Argentina",
            description="This is a course",
            categories=["Programming"],
            presentation_video="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            image="https://static01.nyt.com/images/2017/09/26/science/26TB-PANDA/26TB-PANDA-superJumbo.jpg",
            subscription_id=0,
            recommendations={},
            active=True,
        )

        course.price = price

        assert course.price == price
