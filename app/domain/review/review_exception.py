class UserAlreadyReviewedCourseError(Exception):
    message = "User has reviewed this course already."

    def __str__(self):
        return UserAlreadyReviewedCourseError.message
