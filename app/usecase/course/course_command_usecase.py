from abc import ABC, abstractmethod
from typing import Optional, cast

import shortuuid

from app.domain.course import (
    Course,
    CourseNameAlreadyExistsError,
    CourseNotFoundError,
    CourseRepository,
)

from ..user.user_query_model import UserReadModel
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
    def create_course(
        self, data: CourseCreateModel, creator_id: str
    ) -> Optional[CourseReadModel]:
        raise NotImplementedError

    @abstractmethod
    def update_course(
        self, id: str, data: CourseUpdateModel
    ) -> Optional[CourseReadModel]:
        raise NotImplementedError

    @abstractmethod
    def delete_course_by_id(self, id: str):
        raise NotImplementedError

    @abstractmethod
    def add_user(self, data: UserReadModel) -> Optional[UserReadModel]:
        raise NotImplementedError

    @abstractmethod
    def deactivate_user_from_course(self, user_id: str, course_id: str):
        raise NotImplementedError


class CourseCommandUseCaseImpl(CourseCommandUseCase):
    def __init__(
        self,
        uow: CourseCommandUseCaseUnitOfWork,
    ):
        self.uow: CourseCommandUseCaseUnitOfWork = uow

    def create_course(
        self, data: CourseCreateModel, creator_id: str
    ) -> Optional[CourseReadModel]:
        try:
            uuid = shortuuid.uuid()
            course = Course(
                id=uuid,
                creator_id=creator_id,
                name=data.name,
                price=data.price,
                language=data.language,
                description=data.description,
                categories=data.categories,
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
                creator_id=existing_course.creator_id,
                name=existing_course.name,
                price=data.price,
                language=data.language,
                description=data.description,
                categories=data.categories,
                created_at=existing_course.created_at,
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

    def add_user(self, data: UserReadModel) -> Optional[UserReadModel]:
        try:
            course = self.uow.course_repository.find_by_id(data.course_id)
            if course is None:
                raise CourseNotFoundError
            self.uow.course_repository.add_user(data)
            self.uow.commit()
        except:
            self.uow.rollback()
            raise

        return data

    def deactivate_user_from_course(self, user_id: str, course_id: str):
        try:
            course = self.uow.course_repository.find_by_id(course_id)
            if course is None:
                raise CourseNotFoundError
            self.uow.course_repository.deactivate_user_from_course(user_id, course_id)
            self.uow.commit()
        except:
            self.uow.rollback()
            raise
