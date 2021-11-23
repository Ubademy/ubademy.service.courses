from abc import ABC, abstractmethod
from typing import Optional

from app.domain.course import Course
from app.usecase.collab.collab_query_model import CollabReadModel
from app.usecase.content.content_command_model import (
    ContentCreateModel,
    ContentUpdateModel,
)
from app.usecase.content.content_query_model import ContentReadModel


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

    @abstractmethod
    def add_collab(self, course_id: str, user_id: str) -> Optional[CollabReadModel]:
        raise NotImplementedError

    @abstractmethod
    def deactivate_collab_from_course(self, user_id, course_id):
        raise NotImplementedError

    @abstractmethod
    def add_content(
        self, data: ContentCreateModel, course_id: str
    ) -> Optional[ContentReadModel]:
        raise NotImplementedError

    @abstractmethod
    def update_content_from_course(
        self, course_id: str, data: ContentUpdateModel, content_id: str
    ) -> Optional[ContentReadModel]:
        raise NotImplementedError

    @abstractmethod
    def user_involved(self, course_id: str, user_id: str) -> bool:
        raise NotImplementedError
