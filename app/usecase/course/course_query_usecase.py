from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from app.domain.course import CourseNotFoundError

from ..content.content_query_model import ChapterReadModel
from ..metrics.category_metrics_query_model import CategoryMetricsReadModel
from ..metrics.new_courses_metrics_query_model import NewCoursesMetricsReadModel
from ..metrics.subscriptions_metrics_query_model import SubscriptionMetricsReadModel
from ..review.review_query_model import ReviewReadModel
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
        inactive_courses: Optional[bool],
        inactive_collab: Optional[bool],
        category: Optional[str],
        language: Optional[str],
        country: Optional[str],
        ignore_free: Optional[bool],
        ignore_paid: Optional[bool],
        text: Optional[str],
        limit: int = 100,
        offset: int = 0,
    ) -> Tuple[List[CourseReadModel], int]:
        raise NotImplementedError

    @abstractmethod
    def fetch_content_by_id(self, id: str) -> List[ChapterReadModel]:
        raise NotImplementedError

    @abstractmethod
    def user_is_creator(self, course_id: str, user_id: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def fetch_reviews_by_id(self, id: str) -> List[ReviewReadModel]:
        raise NotImplementedError

    @abstractmethod
    def get_category_metrics(
        self, limit: int
    ) -> Tuple[List[CategoryMetricsReadModel], int]:
        raise NotImplementedError

    @abstractmethod
    def get_course_metrics(self, year) -> NewCoursesMetricsReadModel:
        raise NotImplementedError

    @abstractmethod
    def get_subscription_metrics(self) -> SubscriptionMetricsReadModel:
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
        inactive_courses: Optional[bool] = None,
        inactive_collab: Optional[bool] = None,
        category: Optional[str] = None,
        language: Optional[str] = None,
        country: Optional[str] = None,
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
                inactive_courses=inactive_courses,
                inactive_collab=inactive_collab,
                category=category,
                language=language,
                country=country,
                ignore_free=ignore_free,
                ignore_paid=ignore_paid,
                text=text,
                limit=limit,
                offset=offset,
            )
        except:
            raise

        return courses, count

    def fetch_content_by_id(self, id: str) -> List[ChapterReadModel]:
        try:
            content = self.course_query_service.fetch_content_by_id(id)
            v: List[ChapterReadModel] = []
            chapter = -1
            index = -1
            for c in content:
                if c.chapter != chapter:
                    chapter = c.chapter
                    v.append(ChapterReadModel.from_content_read_model(c))
                    index += 1
                v[index].content.append(c)
        except:
            raise

        return v

    def user_is_creator(self, course_id: str, user_id: str) -> bool:
        course = self.fetch_course_by_id(course_id)
        return course is not None and course.creator_id == user_id

    def fetch_reviews_by_id(self, id: str) -> List[ReviewReadModel]:
        try:
            r = self.course_query_service.fetch_reviews_by_id(id)
        except:
            raise
        return r

    def get_category_metrics(
        self, limit: int
    ) -> Tuple[List[CategoryMetricsReadModel], int]:
        try:
            categories, count = self.course_query_service.get_category_metrics(
                limit=limit
            )
        except:
            raise
        return categories, count

    def get_course_metrics(self, year) -> NewCoursesMetricsReadModel:
        try:
            metrics = self.course_query_service.get_courses_metrics(year=year)
        except:
            raise
        return metrics

    def get_subscription_metrics(self) -> SubscriptionMetricsReadModel:
        try:
            metrics = self.course_query_service.get_subscription_metrics()
        except:
            raise
        return metrics
