from app.domain.course import Course
from app.infrastructure.sqlite.course import CourseDTO


class TestCourseDTO:
    def test_to_read_model_should_create_entity_instance(self):
        course_dto = CourseDTO(
            id="course_1",
            creator_id="creator_1",
            name="C Programming For Beginners - Master the C Language",
            price=10,
            language="English",
            description="This is a course",
            created_at=1614007224642,
            updated_at=9999994444444,
        )

        course = course_dto.to_read_model()

        assert course.id == "course_1"
        assert course.creator_id == "creator_1"
        assert course.name == "C Programming For Beginners - Master the C Language"
        assert course.price == 10
        assert course.language == "English"
        assert course.description == "This is a course"
        assert course.categories == []
        assert course.created_at == 1614007224642
        assert course.updated_at == 9999994444444

    def test_to_entity_should_create_entity_instance(self):
        course_dto = CourseDTO(
            id="course_1",
            creator_id="creator_1",
            name="C Programming For Beginners - Master the C Language",
            price=10,
            language="English",
            description="This is a course",
            created_at=1614007224642,
            updated_at=9999994444444,
        )

        course = course_dto.to_entity()

        assert course.id == "course_1"
        assert course.creator_id == "creator_1"
        assert course.name == "C Programming For Beginners - Master the C Language"
        assert course.price == 10
        assert course.language == "English"
        assert course.description == "This is a course"
        assert course.categories == []
        assert course.created_at == 1614007224642
        assert course.updated_at == 9999994444444

    def test_from_entity_should_create_dto_instance_inits_created_at_updated_at(self):
        course = Course(
            id="course_1",
            creator_id="creator_1",
            name="C Programming For Beginners - Master the C Language",
            price=10,
            language="English",
            description="This is a course",
            categories=[],
        )

        course_dto = CourseDTO.from_entity(course)

        assert course_dto.id == "course_1"
        assert course_dto.creator_id == "creator_1"
        assert course_dto.name == "C Programming For Beginners - Master the C Language"
        assert course_dto.price == 10
        assert course_dto.language == "English"
        assert course_dto.description == "This is a course"
        assert course_dto.created_at == course_dto.updated_at

    def test_from_entity_should_create_dto_instance_preserves_created_at(self):
        course = Course(
            id="course_1",
            creator_id="creator_1",
            name="C Programming For Beginners - Master the C Language",
            price=10,
            language="English",
            description="This is a course",
            categories=[],
            created_at=1614007224642,
            updated_at=9999994444444,
        )

        course_dto = CourseDTO.from_entity(course)

        assert course_dto.id == "course_1"
        assert course_dto.creator_id == "creator_1"
        assert course_dto.name == "C Programming For Beginners - Master the C Language"
        assert course_dto.price == 10
        assert course_dto.language == "English"
        assert course_dto.description == "This is a course"
        assert course_dto.created_at == 1614007224642
