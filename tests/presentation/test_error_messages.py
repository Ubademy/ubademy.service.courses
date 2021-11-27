from app.presentation.schema.collab.collab_error_message import (
    ErrorMessageNoCollabsInCourse,
    ErrorMessageUserAlreadyInCourse,
)
from app.presentation.schema.content.content_error_message import ErrorMessageChapterAlreadyInCourse
from app.presentation.schema.course.course_error_message import (
    ErrorMessageCategoriesNotFound,
    ErrorMessageCourseNameAlreadyExists,
    ErrorMessageCourseNotFound,
    ErrorMessageCoursesNotFound,
)
from app.presentation.schema.review.review_error_message import ErrorMessageUserAlreadyReviewedCourse


class TestErrorMessages:
    def test_error_messages(self):
        assert ErrorMessageCourseNotFound is not ErrorMessageCourseNameAlreadyExists
        assert ErrorMessageCoursesNotFound is not ErrorMessageCategoriesNotFound
        assert ErrorMessageUserAlreadyInCourse is not ErrorMessageNoCollabsInCourse
        assert ErrorMessageChapterAlreadyInCourse is not ErrorMessageUserAlreadyReviewedCourse

