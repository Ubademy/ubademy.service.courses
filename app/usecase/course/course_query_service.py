from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from ..collab.collab_query_model import CollabReadModel
from ..content.content_query_model import ContentReadModel
from ..metrics.category_metrics_query_model import CategoryMetricsReadModel
from ..metrics.new_courses_metrics_query_model import NewCoursesMetricsReadModel
from ..metrics.susbcriptions_metrics_query_model import SubscriptionMetricsReadModel
from ..review.review_query_model import ReviewReadModel
from .course_query_model import CourseReadModel


class CourseQueryService(ABC):
    @abstractmethod
    def find_by_id(self, id: str) -> Optional[CourseReadModel]:
        raise NotImplementedError

    @abstractmethod
    def find_all(
        self, limit: int = 100, offset: int = 0
    ) -> Tuple[List[CourseReadModel], int]:
        raise NotImplementedError

    @abstractmethod
    def find_all_categories(self) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def find_by_filters(
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
    def find_collabs_by_id(self, id: str) -> List[CollabReadModel]:
        raise NotImplementedError

    @abstractmethod
    def fetch_content_by_id(self, id: str) -> List[ContentReadModel]:
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
    def get_courses_metrics(self, year) -> NewCoursesMetricsReadModel:
        raise NotImplementedError

    @abstractmethod
    def get_subscription_metrics(self) -> SubscriptionMetricsReadModel:
        raise NotImplementedError
