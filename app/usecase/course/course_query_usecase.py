from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.course import CourseNotFoundError

from ..content.content_query_model import ContentReadModel
from .course_query_model import CourseReadModel
from .course_query_service import CourseQueryService


class CourseQueryUseCase(ABC):
    @abstractmethod
    def fetch_course_by_id(self, id: str) -> Optional[CourseReadModel]:
        raise NotImplementedError

    @abstractmethod
    def fetch_courses(self) -> List[CourseReadModel]:
        raise NotImplementedError

    @abstractmethod
    def fetch_categories(self):
        raise NotImplementedError

    @abstractmethod
    def fetch_courses_by_filters(
        self,
        name: Optional[str],
        creator_id: Optional[str],
        colab_id: Optional[str],
        inactive: Optional[bool],
        category: Optional[str],
        language: Optional[str],
        ignore_free: Optional[bool],
        ignore_paid: Optional[bool],
        text: Optional[str],
    ) -> List[CourseReadModel]:
        raise NotImplementedError

    @abstractmethod
    def fetch_content_by_id(self, id: str) -> List[ContentReadModel]:
        raise NotImplementedError

    @abstractmethod
    def user_is_creator(self, course_id: str, user_id: str) -> bool:
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

    def fetch_categories(self) -> List[str]:
        try:
            categories = self.course_query_service.find_all_categories()
        except:
            raise

        return categories

    def fetch_courses_by_filters(
        self,
        name: Optional[str] = None,
        creator_id: Optional[str] = None,
        colab_id: Optional[str] = None,
        inactive: Optional[bool] = None,
        category: Optional[str] = None,
        language: Optional[str] = None,
        ignore_free: Optional[bool] = None,
        ignore_paid: Optional[bool] = None,
        text: Optional[str] = None,
    ) -> List[CourseReadModel]:
        try:
            courses = self.course_query_service.find_by_filters(
                name=name,
                creator_id=creator_id,
                colab_id=colab_id,
                inactive=inactive,
                category=category,
                language=language,
                ignore_free=ignore_free,
                ignore_paid=ignore_paid,
                text=text,
            )
        except:
            raise

        return courses

    def fetch_content_by_id(self, id: str) -> List[ContentReadModel]:
        try:
            content = self.course_query_service.fetch_content_by_id(id)
        except:
            raise

        return content

    def user_is_creator(self, course_id: str, user_id: str) -> bool:
        course = self.fetch_course_by_id(course_id)
        return course is not None and course.creator_id == user_id
