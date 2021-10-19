from abc import ABC, abstractmethod
from typing import Optional

from app.domain.course import Course


class CourseRepository(ABC):
    @abstractmethod
    def create(self, course: Course) -> Optional[Course]:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, id: str) -> Optional[Course]:
        raise NotImplementedError

    @abstractmethod
    def find_by_name(self, name: str) -> Optional[Course]:
        raise NotImplementedError

    @abstractmethod
    def update(self, course: Course) -> Optional[Course]:
        raise NotImplementedError

    @abstractmethod
    def delete_by_id(self, id: str):
        raise NotImplementedError
