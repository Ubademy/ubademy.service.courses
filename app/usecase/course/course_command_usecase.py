from abc import ABC, abstractmethod
from typing import Optional, cast

import shortuuid

from app.domain.course import (
    Course,
    CourseNameAlreadyExistsError,
    CourseNotFoundError,
    CourseRepository,
)

from .course_command_model import CourseCreateModel, CourseUpdateModel
from .course_query_model import CourseReadModel


class CourseCommandUseCaseUnitOfWork(ABC):

    course_repository: CourseRepository

    @abstractmethod
    def begin(self):
        raise NotImplementedError

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError


class CourseCommandUseCase(ABC):
    @abstractmethod
    def create_course(self, data: CourseCreateModel) -> Optional[CourseReadModel]:
        raise NotImplementedError

    @abstractmethod
    def update_course(
        self, id: str, data: CourseUpdateModel
    ) -> Optional[CourseReadModel]:
        raise NotImplementedError

    @abstractmethod
    def delete_course_by_id(self, id: str):
        raise NotImplementedError


class CourseCommandUseCaseImpl(CourseCommandUseCase):
    def __init__(
        self,
        uow: CourseCommandUseCaseUnitOfWork,
    ):
        self.uow: CourseCommandUseCaseUnitOfWork = uow

    def create_course(self, data: CourseCreateModel) -> Optional[CourseReadModel]:
        try:
            uuid = shortuuid.uuid()
            course = Course(
                id=uuid, name=data.name, categories=data.categories, price=data.price
            )

            existing_course = self.uow.course_repository.find_by_name(data.name)
            if existing_course is not None:
                raise CourseNameAlreadyExistsError
            self.uow.course_repository.create(course)
            self.uow.commit()

            created_course = self.uow.course_repository.find_by_id(uuid)
        except:
            self.uow.rollback()
            raise

        return CourseReadModel.from_entity(cast(Course, created_course))

    def update_course(
        self, id: str, data: CourseUpdateModel
    ) -> Optional[CourseReadModel]:
        try:
            existing_course = self.uow.course_repository.find_by_id(id)
            if existing_course is None:
                raise CourseNotFoundError

            course = Course(
                id=id,
                name=existing_course.name,
                categories=data.categories,
                price=data.price,
            )

            self.uow.course_repository.update(course)

            updated_course = self.uow.course_repository.find_by_id(course.id)

            self.uow.commit()
        except:
            self.uow.rollback()
            raise

        return CourseReadModel.from_entity(cast(Course, updated_course))

    def delete_course_by_id(self, id: str):
        try:
            existing_course = self.uow.course_repository.find_by_id(id)
            if existing_course is None:
                raise CourseNotFoundError

            self.uow.course_repository.delete_by_id(id)

            self.uow.commit()
        except:
            self.uow.rollback()
            raise
