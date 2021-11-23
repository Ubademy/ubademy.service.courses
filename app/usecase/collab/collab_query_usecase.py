from abc import ABC, abstractmethod
from typing import List

from app.domain.collab.collab_exception import NoCollabsInCourseError
from app.usecase.course import CourseQueryService


class CollabQueryUseCase(ABC):
    @abstractmethod
    def fetch_collabs_by_id(self, id: str) -> List[str]:
        raise NotImplementedError


class CollabQueryUseCaseImpl(CollabQueryUseCase):
    def __init__(self, course_query_service: CourseQueryService):
        self.course_query_service: CourseQueryService = course_query_service

    def fetch_collabs_by_id(self, id: str) -> List[str]:
        try:
            collabs = self.course_query_service.find_collabs_by_id(id)
            r = list(map(lambda collab: collab.get_id(), collabs))
            if len(r) == 0:
                raise NoCollabsInCourseError
        except:
            raise

        return r
