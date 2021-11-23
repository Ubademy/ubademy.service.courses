class NoCollabsInCourseError(Exception):
    message = "The course you specified has no collaborators working."

    def __str__(self):
        return NoCollabsInCourseError.message


class UserAlreadyInCourseError(Exception):
    message = "The course you specified already has an active collab with that id."

    def __str__(self):
        return UserAlreadyInCourseError.message


class UserIsNotCreatorError(Exception):
    message = "User is not the creator of the course you specified."

    def __str__(self):
        return UserIsNotCreatorError.message
