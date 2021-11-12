class NoUsersInCourseError(Exception):
    message = "The course you specified has no users involved."

    def __str__(self):
        return NoUsersInCourseError.message


class NoColabsInCourseError(Exception):
    message = "The course you specified has no collaborators working."

    def __str__(self):
        return NoColabsInCourseError.message


class NoStudentsInCourseError(Exception):
    message = "The course you specified has no active students."

    def __str__(self):
        return NoStudentsInCourseError.message


class UserAlreadyInCourseError(Exception):
    message = "The course you specified already has an active user with that id."

    def __str__(self):
        return UserAlreadyInCourseError.message


class UserIsNotCreatorError(Exception):
    message = "User is not the creator of the course you specified."

    def __str__(self):
        return UserIsNotCreatorError.message
