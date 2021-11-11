class ChapterAlreadyInCourseError(Exception):
    message = (
        "The course you specified already has content with the chapter you specified."
    )

    def __str__(self):
        return ChapterAlreadyInCourseError.message


class ContentNotFoundError(Exception):
    message = "The content you specified does not exist."

    def __str__(self):
        return ContentNotFoundError.message
