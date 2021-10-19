from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.course import CourseNotFoundError

from .course_query_model import CourseReadModel
from .course_query_service import CourseQueryService


class CourseQueryUseCase(ABC):
    @abstractmethod
    def fetch_course_by_id(self, id: str) -> Optional[CourseReadModel]:
        raise NotImplementedError

    @abstractmethod
    def fetch_courses(self) -> List[CourseReadModel]:
        raise NotImplementedError


class CourseQueryUseCaseImpl(CourseQueryUseCase):
    def __init__(self, course_query_service: CourseQueryService):
        self.course_query_service: CourseQueryService = course_query_service

    def fetch_course_by_id(self, id: str) -> Optional[CourseReadModel]:
        try:
            course = self.course_query_service.find_by_id(id)
            if course is None:
                raise CourseNotFoundError
        except:
            raise

        return course

    def fetch_courses(self) -> List[CourseReadModel]:
        try:
            courses = self.course_query_service.find_all()
        except:
            raise

        return courses
