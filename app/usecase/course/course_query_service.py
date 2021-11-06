from abc import ABC, abstractmethod
from typing import List, Optional

from ..user.user_query_model import UserReadModel
from .course_query_model import CourseReadModel


class CourseQueryService(ABC):
    @abstractmethod
    def find_by_id(self, id: str) -> Optional[CourseReadModel]:
        raise NotImplementedError

    @abstractmethod
    def find_all(self) -> List[CourseReadModel]:
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
    def find_users_by_id(self, id: str) -> List[UserReadModel]:
        raise NotImplementedError
