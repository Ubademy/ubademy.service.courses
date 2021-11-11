from abc import ABC, abstractmethod
from typing import List, Optional

from ..content.content_query_model import ContentReadModel
from ..user.user_query_model import MiniUserReadModel
from .course_query_model import CourseReadModel


class CourseQueryService(ABC):
    @abstractmethod
    def find_by_id(self, id: str) -> Optional[CourseReadModel]:
        raise NotImplementedError

    @abstractmethod
    def find_all(self) -> List[CourseReadModel]:
        raise NotImplementedError

    @abstractmethod
    def find_all_categories(self) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def find_by_filters(
        self,
        name: Optional[str],
        creator_id: Optional[str],
        colab_id: Optional[str],
        category: Optional[str],
        language: Optional[str],
        ignore_free: Optional[bool],
        ignore_paid: Optional[bool],
        text: Optional[str],
    ) -> List[CourseReadModel]:
        raise NotImplementedError

    @abstractmethod
    def find_users_by_id(self, id: str) -> List[MiniUserReadModel]:
        raise NotImplementedError

    @abstractmethod
    def fetch_content_by_id(self, id: str) -> List[ContentReadModel]:
        raise NotImplementedError
