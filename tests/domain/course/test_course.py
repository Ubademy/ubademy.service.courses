import pytest

from app.domain.course import Course


class TestCourse:
    def test_constructor_should_create_instance(self):
        course = Course(
            id="course_01",
            name="C Programming For Beginners - Master the C Language",
            categories="Programming",
            price=10,
        )

        assert course.id == "course_01"
        assert course.name == "C Programming For Beginners - Master the C Language"
        assert course.categories == "Programming"
        assert course.price == 10

    def test_course_entity_should_be_identified_by_id(self):
        course_1 = Course(
            id="course_01",
            name="C Programming For Beginners - Master the C Language",
            categories="Programming",
            price=10,
        )

        course_2 = Course(
            id="course_01",
            name="C Programming For Beginners - Master the C Language",
            categories="Programming",
            price=10,
        )

        course_3 = Course(
            id="course_02",
            name="Learn Python Programming Masterclass",
            categories="Programming",
            price=20,
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
            id="course_01",
            name="C Programming For Beginners - Master the C Language",
            categories="Programming",
            price=10,
        )

        course.price = price

        assert course.price == price
