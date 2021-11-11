class ChapterAlreadyInCourseError(Exception):
    message = (
        "The course you specified already has content with the chapter you specified."
    )

    def __str__(self):
        return ChapterAlreadyInCourseError.message
