from abc import ABC, abstractmethod
from typing import Optional, cast

import shortuuid

from app.domain.course import (
    Course,
    CourseNameAlreadyExistsError,
    CourseNotFoundError,
    CourseRepository,
)

from ...domain.review.review import Review
from ..collab.collab_query_model import CollabReadModel
from ..content.content_command_model import ContentCreateModel, ContentUpdateModel
from ..content.content_query_model import ContentReadModel
from ..review.review_command_model import ReviewCreateModel
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
    def add_collab(self, course_id: str, user_id: str) -> Optional[CollabReadModel]:
        raise NotImplementedError

    @abstractmethod
    def deactivate_collab_from_course(self, user_id: str, course_id: str):
        raise NotImplementedError

    @abstractmethod
    def add_content(self, data, course_id):
        raise NotImplementedError

    @abstractmethod
    def update_content(
        self, course_id: str, data: ContentUpdateModel, content_id: str
    ) -> Optional[ContentReadModel]:
        raise NotImplementedError

    @abstractmethod
    def user_involved(self, course_id: str, user_id: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def add_review(self, id: str, data: ReviewCreateModel):
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
                presentation_video=data.presentation_video,
                image=data.image,
                subscription_id=data.subscription_id,
                recommendations={},
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
                name=data.name,
                price=data.price,
                language=data.language,
                description=data.description,
                categories=data.categories,
                presentation_video=data.presentation_video,
                image=data.image,
                recommendations={},
                subscription_id=data.subscription_id,
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

    def add_collab(self, course_id: str, user_id: str) -> Optional[CollabReadModel]:
        try:
            course = self.uow.course_repository.find_by_id(course_id)
            if course is None:
                raise CourseNotFoundError
            collab = self.uow.course_repository.add_collab(
                course_id=course_id, user_id=user_id
            )
            self.uow.commit()
        except:
            self.uow.rollback()
            raise

        return collab

    def deactivate_collab_from_course(self, user_id: str, course_id: str):
        try:
            course = self.uow.course_repository.find_by_id(course_id)
            if course is None:
                raise CourseNotFoundError
            self.uow.course_repository.deactivate_collab_from_course(user_id, course_id)
            self.uow.commit()
        except:
            self.uow.rollback()
            raise

    def add_content(
        self, data: ContentCreateModel, course_id: str
    ) -> Optional[ContentReadModel]:
        try:
            course = self.uow.course_repository.find_by_id(course_id)
            if course is None:
                raise CourseNotFoundError
            content = self.uow.course_repository.add_content(
                data=data, course_id=course_id
            )
            self.uow.commit()
        except:
            self.uow.rollback()
            raise

        return content

    def update_content(
        self, course_id: str, data: ContentUpdateModel, content_id: str
    ) -> Optional[ContentReadModel]:
        try:
            existing_course = self.uow.course_repository.find_by_id(course_id)
            if existing_course is None:
                raise CourseNotFoundError
            updated_content = self.uow.course_repository.update_content_from_course(
                course_id=course_id, data=data, content_id=content_id
            )
            self.uow.commit()
        except:
            self.uow.rollback()
            raise

        return updated_content

    def user_involved(self, course_id: str, user_id: str) -> bool:
        return self.uow.course_repository.user_involved(
            course_id=course_id, user_id=user_id
        )

    def add_review(self, id: str, data: ReviewCreateModel):
        try:
            existing_course = self.uow.course_repository.find_by_id(id)
            if existing_course is None:
                raise CourseNotFoundError
            rev = Review(
                id=data.id,
                course_id=id,
                recommended=data.recommended,
                review=data.review,
            )
            review = self.uow.course_repository.add_review(review=rev)
            self.uow.commit()
        except:
            self.uow.rollback()
            raise

        return review
