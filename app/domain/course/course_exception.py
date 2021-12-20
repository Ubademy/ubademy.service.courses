class CourseNotFoundError(Exception):
    message = "The course you specified does not exist."

    def __str__(self):
        return CourseNotFoundError.message


class CourseNameAlreadyExistsError(Exception):
    message = "A course with the name you specified already exists."

    def __str__(self):
        return CourseNameAlreadyExistsError.message


class CoursesNotFoundError(Exception):
    message = "No courses were found."

    def __str__(self):
        return CoursesNotFoundError.message


class CategoriesNotFoundError(Exception):
    message = "No categories were found."

    def __str__(self):
        return CategoriesNotFoundError.message


class NotEnoughFundsError(Exception):
    message = "Creator does not have enough funds to cancel course."

    def __str__(self):
        return NotEnoughFundsError.message
