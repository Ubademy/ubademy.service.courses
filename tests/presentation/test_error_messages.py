from app.presentation.schema.collab.collab_error_message import (
    ErrorMessageNoCollabsInCourse,
    ErrorMessageUserAlreadyInCourse,
)
from app.presentation.schema.course.course_error_message import (
    ErrorMessageCategoriesNotFound,
    ErrorMessageCourseNameAlreadyExists,
    ErrorMessageCourseNotFound,
    ErrorMessageCoursesNotFound,
)


class TestErrorMessages:
    def test_error_messages(self):
        assert ErrorMessageCourseNotFound is not ErrorMessageCourseNameAlreadyExists
        assert ErrorMessageCoursesNotFound is not ErrorMessageCategoriesNotFound
        assert ErrorMessageUserAlreadyInCourse is not ErrorMessageNoCollabsInCourse
