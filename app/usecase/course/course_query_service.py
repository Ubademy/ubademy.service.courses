from abc import ABC, abstractmethod
from typing import List, Optional

from .course_query_model import CourseReadModel


class CourseQueryService(ABC):
    @abstractmethod
    def find_by_id(self, id: str) -> Optional[CourseReadModel]:
        raise NotImplementedError

    @abstractmethod
    def find_all(self) -> List[CourseReadModel]:
        raise NotImplementedError
