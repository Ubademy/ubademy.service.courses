from abc import ABC, abstractmethod
from typing import List

from app.domain.user.user_exception import (
    NoColabsInCourseError,
    NoStudentsInCourseError,
)
from app.usecase.course import CourseQueryService


class UserQueryUseCase(ABC):
    @abstractmethod
    def fetch_students_by_id(self, id: str) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def fetch_colabs_by_id(self, id: str) -> List[str]:
        raise NotImplementedError


class UserQueryUseCaseImpl(UserQueryUseCase):
    def __init__(self, course_query_service: CourseQueryService):
        self.course_query_service: CourseQueryService = course_query_service

    def fetch_students_by_id(self, id: str) -> List[str]:
        try:
            users = self.course_query_service.find_users_by_id(id)
            students = list(filter(lambda user: user.is_student(), users))
            r = list(map(lambda user: user.get_id(), students))
            if len(students) == 0:
                raise NoStudentsInCourseError
        except:
            raise

        return r

    def fetch_colabs_by_id(self, id: str) -> List[str]:
        try:
            users = self.course_query_service.find_users_by_id(id)
            colabs = list(filter(lambda user: user.is_colab(), users))
            r = list(map(lambda user: user.get_id(), colabs))
            if len(colabs) == 0:
                raise NoColabsInCourseError
        except:
            raise

        return r
