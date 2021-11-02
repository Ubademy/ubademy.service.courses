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
    message = "The course you specified already has a student with that id."

    def __str__(self):
        return UserAlreadyInCourseError.message