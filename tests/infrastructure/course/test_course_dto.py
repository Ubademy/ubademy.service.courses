from app.domain.course import Course
from app.infrastructure.course import CourseDTO
from app.infrastructure.course.course_dto import Category


class TestCourseDTO:
    def test_to_read_model_should_create_entity_instance(self):
        course_dto = CourseDTO(
            id="course_1",
            creator_id="creator_1",
            name="C Programming For Beginners - Master the C Language",
            price=10,
            subscription_id=0,
            language="English",
            country="Argentina",
            description="This is a course",
            categories=[Category(category="Programing")],
            presentation_video="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            image="https://static01.nyt.com/images/2017/09/26/science/26TB-PANDA/26TB-PANDA-superJumbo.jpg",
            created_at=1614007224642,
            updated_at=9999994444444,
            active=True,
        )

        course = course_dto.to_read_model()

        assert course.id == "course_1"
        assert course.creator_id == "creator_1"
        assert course.name == "C Programming For Beginners - Master the C Language"
        assert course.price == 10
        assert course.language == "English"
        assert course.description == "This is a course"
        assert course.categories == ["Programing"]
        assert (
            course.presentation_video == "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        )
        assert course.created_at == 1614007224642
        assert course.updated_at == 9999994444444

    def test_to_entity_should_create_entity_instance(self):
        course_dto = CourseDTO(
            id="course_1",
            creator_id="creator_1",
            name="C Programming For Beginners - Master the C Language",
            price=10,
            language="English",
            country="Argentina",
            description="This is a course",
            categories=[Category(category="Programing"), Category(category="Beginner")],
            presentation_video="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            image="https://static01.nyt.com/images/2017/09/26/science/26TB-PANDA/26TB-PANDA-superJumbo.jpg",
            created_at=1614007224642,
            updated_at=9999994444444,
            active=True,
        )

        course = course_dto.to_entity()

        assert course.id == "course_1"
        assert course.creator_id == "creator_1"
        assert course.name == "C Programming For Beginners - Master the C Language"
        assert course.price == 10
        assert course.language == "English"
        assert course.description == "This is a course"
        assert course.categories == ["Programing", "Beginner"]
        assert (
            course.presentation_video == "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        )
        assert course.created_at == 1614007224642
        assert course.updated_at == 9999994444444

    def test_from_entity_should_create_dto_instance_inits_created_at_updated_at(self):
        course = Course(
            id="course_1",
            creator_id="creator_1",
            name="C Programming For Beginners - Master the C Language",
            price=10,
            language="English",
            country="Argentina",
            description="This is a course",
            categories=["Programing", "Beginner"],
            presentation_video="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            image="https://static01.nyt.com/images/2017/09/26/science/26TB-PANDA/26TB-PANDA-superJumbo.jpg",
            subscription_id=0,
            recommendations={},
            active=True,
        )

        course_dto = CourseDTO.from_entity(course)

        assert course_dto.id == "course_1"
        assert course_dto.creator_id == "creator_1"
        assert course_dto.name == "C Programming For Beginners - Master the C Language"
        assert course_dto.price == 10
        assert course_dto.language == "English"
        assert course_dto.description == "This is a course"
        assert course_dto.created_at == course_dto.updated_at
        assert course_dto.get_categories() == ["Programing", "Beginner"]
        assert (
            course_dto.presentation_video
            == "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        )

    def test_from_entity_should_create_dto_instance_preserves_created_at(self):
        course = Course(
            id="course_1",
            creator_id="creator_1",
            name="C Programming For Beginners - Master the C Language",
            price=10,
            language="English",
            country="Argentina",
            description="This is a course",
            categories=["Programing"],
            presentation_video="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            image="https://static01.nyt.com/images/2017/09/26/science/26TB-PANDA/26TB-PANDA-superJumbo.jpg",
            subscription_id=0,
            created_at=1614007224642,
            updated_at=9999994444444,
            recommendations={},
            active=True,
        )

        course_dto = CourseDTO.from_entity(course)

        assert course_dto.id == "course_1"
        assert course_dto.creator_id == "creator_1"
        assert course_dto.name == "C Programming For Beginners - Master the C Language"
        assert course_dto.price == 10
        assert course_dto.language == "English"
        assert course_dto.description == "This is a course"
        assert course_dto.created_at == 1614007224642
        assert course_dto.get_categories() == ["Programing"]
        assert (
            course_dto.presentation_video
            == "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        )
        assert (
            course_dto.image
            == "https://static01.nyt.com/images/2017/09/26/science/26TB-PANDA/26TB-PANDA-superJumbo.jpg"
        )
