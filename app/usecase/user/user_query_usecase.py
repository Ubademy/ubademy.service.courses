from abc import ABC, abstractmethod
from typing import List

from app.domain.user.user_exception import (
    NoColabsInCourseError,
    NoStudentsInCourseError,
)
from app.usecase.course import CourseQueryService
from app.usecase.user.user_query_model import UserReadModel


class UserQueryUseCase(ABC):
    @abstractmethod
    def fetch_students_by_id(self, id: str) -> List[UserReadModel]:
        raise NotImplementedError

    @abstractmethod
    def fetch_colabs_by_id(self, id: str) -> List[UserReadModel]:
        raise NotImplementedError


class UserQueryUseCaseImpl(UserQueryUseCase):
    def __init__(self, course_query_service: CourseQueryService):
        self.course_query_service: CourseQueryService = course_query_service

    def fetch_students_by_id(self, id: str) -> List[UserReadModel]:
        try:
            users = self.course_query_service.find_users_by_id(id)
            students = list(filter(lambda user: user.is_student(), users))
            if len(students) == 0:
                raise NoStudentsInCourseError
        except:
            raise

        return students

    def fetch_colabs_by_id(self, id: str) -> List[UserReadModel]:
        try:
            users = self.course_query_service.find_users_by_id(id)
            colabs = list(filter(lambda user: user.is_colab(), users))
            if len(colabs) == 0:
                raise NoColabsInCourseError
        except:
            raise

        return colabs
