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
            description="This is a course",
            categories=["Programming"],
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
            description="This is a course",
            categories=["Programming"],
        )

        course_2 = Course(
            id="course_1",
            creator_id="creator_1",
            name="Learn Python Programming Masterclass",
            price=20,
            language="English",
            description="This is a course",
            categories=["Programming"],
        )

        course_3 = Course(
            id="course_3",
            creator_id="creator_1",
            name="C Programming For Beginners - Master the C Language",
            price=10,
            language="English",
            description="This is a course",
            categories=["Programming"],
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
            description="This is a course",
            categories=["Programming"],
        )

        course.price = price

        assert course.price == price
