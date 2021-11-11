from app.presentation.schema.course.course_error_message import (
    ErrorMessageCategoriesNotFound,
    ErrorMessageCourseNameAlreadyExists,
    ErrorMessageCourseNotFound,
    ErrorMessageCoursesNotFound,
)
from app.presentation.schema.user.user_error_message import (
    ErrorMessageNoColabsInCourse,
    ErrorMessageNoStudentsInCourse,
    ErrorMessageNoUsersInCourse,
    ErrorMessageUserAlreadyInCourse,
)


class TestErrorMessages:
    def test_error_messages(self):
        assert ErrorMessageCourseNotFound is not ErrorMessageCourseNameAlreadyExists
        assert ErrorMessageCoursesNotFound is not ErrorMessageCategoriesNotFound
        assert ErrorMessageNoUsersInCourse is not ErrorMessageNoColabsInCourse
        assert ErrorMessageNoStudentsInCourse is not ErrorMessageUserAlreadyInCourse
