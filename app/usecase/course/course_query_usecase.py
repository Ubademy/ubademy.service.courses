from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from app.domain.course import CourseNotFoundError

from ..content.content_query_model import ContentReadModel
from .course_query_model import CourseReadModel
from .course_query_service import CourseQueryService


class CourseQueryUseCase(ABC):
    @abstractmethod
    def fetch_course_by_id(self, id: str) -> Optional[CourseReadModel]:
        raise NotImplementedError

    @abstractmethod
    def fetch_courses(
        self, limit: int = 100, offset: int = 0
    ) -> Tuple[List[CourseReadModel], int]:
        raise NotImplementedError

    @abstractmethod
    def fetch_categories(self):
        raise NotImplementedError

    @abstractmethod
    def fetch_courses_by_filters(
        self,
        ids: Optional[List[str]],
        name: Optional[str],
        creator_id: Optional[str],
        collab_id: Optional[str],
        subscription_id: Optional[int],
        inactive: Optional[bool],
        category: Optional[str],
        language: Optional[str],
        ignore_free: Optional[bool],
        ignore_paid: Optional[bool],
        text: Optional[str],
        limit: int = 100,
        offset: int = 0,
    ) -> Tuple[List[CourseReadModel], int]:
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

    def fetch_courses(
        self, limit: int = 100, offset: int = 0
    ) -> Tuple[List[CourseReadModel], int]:
        try:
            courses, count = self.course_query_service.find_all(
                limit=limit, offset=offset
            )
        except:
            raise

        return courses, count

    def fetch_categories(self) -> List[str]:
        try:
            categories = self.course_query_service.find_all_categories()
        except:
            raise

        return categories

    def fetch_courses_by_filters(
        self,
        ids: Optional[List[str]] = None,
        name: Optional[str] = None,
        creator_id: Optional[str] = None,
        collab_id: Optional[str] = None,
        subscription_id: Optional[int] = None,
        inactive: Optional[bool] = None,
        category: Optional[str] = None,
        language: Optional[str] = None,
        ignore_free: Optional[bool] = None,
        ignore_paid: Optional[bool] = None,
        text: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> Tuple[List[CourseReadModel], int]:
        try:
            courses, count = self.course_query_service.find_by_filters(
                ids=ids,
                name=name,
                creator_id=creator_id,
                collab_id=collab_id,
                subscription_id=subscription_id,
                inactive=inactive,
                category=category,
                language=language,
                ignore_free=ignore_free,
                ignore_paid=ignore_paid,
                text=text,
                limit=limit,
                offset=offset,
            )
        except:
            raise

        return courses, count

    def fetch_content_by_id(self, id: str) -> List[ContentReadModel]:
        try:
            content = self.course_query_service.fetch_content_by_id(id)
        except:
            raise

        return content

    def user_is_creator(self, course_id: str, user_id: str) -> bool:
        course = self.fetch_course_by_id(course_id)
        return course is not None and course.creator_id == user_id
