from app.domain.course import Course
from app.infrastructure.sqlite.course import CourseDTO


class TestCourseDTO:
    def test_to_read_model_should_create_entity_instance(self):
        course_dto = CourseDTO(
            id="course_01",
            name="C Programming For Beginners - Master the C Language",
            categories="Programming",
            price=10,
            created_at=1614007224642,
            updated_at=1614007224642,
        )

        course = course_dto.to_read_model()

        assert course.id == "course_01"
        assert course.name == "C Programming For Beginners - Master the C Language"
        assert course.categories == "Programming"
        assert course.price == 10

    def test_to_entity_should_create_entity_instance(self):
        course_dto = CourseDTO(
            id="course_01",
            name="C Programming For Beginners - Master the C Language",
            categories="Programming",
            price=10,
            created_at=1614007224642,
            updated_at=1614007224642,
        )

        course = course_dto.to_entity()

        assert course.id == "course_01"
        assert course.name == "C Programming For Beginners - Master the C Language"
        assert course.categories == "Programming"
        assert course.price == 10

    def test_from_entity_should_create_dto_instance(self):
        course = Course(
            id="course_01",
            name="C Programming For Beginners - Master the C Language",
            categories="Programming",
            price=10,
            created_at=1614007224642,
            updated_at=1614007224642,
        )

        course_dto = CourseDTO.from_entity(course)

        assert course_dto.id == "course_01"
        assert course_dto.name == "C Programming For Beginners - Master the C Language"
        assert course_dto.categories == "Programming"
        assert course_dto.price == 10
