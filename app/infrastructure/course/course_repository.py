from typing import Optional

import shortuuid
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from app.domain.collab.collab_exception import UserAlreadyInCourseError
from app.domain.course import Course, CourseNotFoundError, CourseRepository
from app.usecase.collab.collab_query_model import CollabReadModel
from app.usecase.course import CourseCommandUseCaseUnitOfWork

from ...domain.content.content_exception import (
    ChapterAlreadyInCourseError,
    ContentNotFoundError,
)
from ...domain.review.review import Review
from ...domain.review.review_exception import UserAlreadyReviewedCourseError
from ...usecase.content.content_command_model import (
    ContentCreateModel,
    ContentUpdateModel,
)
from ...usecase.content.content_query_model import ContentReadModel
from .course_dto import Category, Collab, Content, CourseDTO, ReviewDTO


class CourseRepositoryImpl(CourseRepository):
    def __init__(self, session: Session):
        self.session: Session = session

    def find_by_id(self, id: str) -> Optional[Course]:
        try:
            course_dto = self.session.query(CourseDTO).filter_by(id=id).one()
        except NoResultFound:
            return None
        except:
            raise

        return course_dto.to_entity()

    def find_by_name(self, name: str) -> Optional[Course]:
        try:
            course_dto = self.session.query(CourseDTO).filter_by(name=name).one()
        except NoResultFound:
            return None
        except:
            raise

        return course_dto.to_entity()

    def create(self, course: Course):
        course_dto = CourseDTO.from_entity(course)
        try:
            self.session.add(course_dto)
        except:
            raise

    def update(self, course: Course):
        course_dto = CourseDTO.from_entity(course)
        try:
            _course: CourseDTO = (
                self.session.query(CourseDTO).filter_by(id=course_dto.id).one()
            )
            if course_dto.name:
                _course.name = course_dto.name
            if course_dto.language:
                _course.language = course_dto.language
            if course_dto.price is not None:
                _course.price = course_dto.price
            if course_dto.subscription_id is not None:
                _course.subscription_id = course_dto.subscription_id
            if course_dto.description:
                _course.description = course_dto.description
            _course.updated_at = course_dto.updated_at
            if course_dto.categories:
                self.session.query(Category).filter_by(course_id=course_dto.id).delete()
                _course.categories = course_dto.categories
            if course_dto.presentation_video:
                _course.presentation_video = course_dto.presentation_video
            if course_dto.image:
                _course.image = course_dto.image
        except:
            raise

    def delete_by_id(self, id: str):
        try:
            course = self.session.query(CourseDTO).filter_by(id=id).first()
            self.session.delete(course)
        except:
            raise

    def add_collab(self, course_id: str, user_id: str) -> Optional[CollabReadModel]:
        try:
            course = self.session.query(CourseDTO).filter_by(id=course_id).first()
            if course.has_active_collab_with_id(user_id):
                raise UserAlreadyInCourseError
            user = CollabReadModel(id=user_id, course_id=course_id, active=True)
            course.collabs.append(Collab.from_read_model(user))
        except NoResultFound:
            raise CourseNotFoundError
        return user

    def deactivate_collab_from_course(self, user_id, course_id):
        try:
            collabs = (
                self.session.query(Collab)
                .filter_by(user_id=user_id, course_id=course_id)
                .all()
            )
            for i in collabs:
                i.deactivate()
        except:
            raise

    def add_content(
        self, data: ContentCreateModel, course_id: str
    ) -> Optional[ContentReadModel]:
        try:
            uuid = shortuuid.uuid()
            course = self.session.query(CourseDTO).filter_by(id=course_id).first()
            if course.has_content_with_chapter(data.chapter, data.order):
                raise ChapterAlreadyInCourseError
            content = Content.from_create_model(
                id=uuid, content=data, course_id=course_id
            )
            course.content.append(content)
        except NoResultFound:
            raise CourseNotFoundError
        return content.to_read_model()

    def update_content_from_course(
        self, course_id: str, data: ContentUpdateModel, content_id: str
    ) -> Optional[ContentReadModel]:
        try:
            _cont = self.session.query(Content).filter_by(id=content_id).first()
            if not _cont:
                raise ContentNotFoundError
            if data.title:
                _cont.title = data.title
            if data.active is not None:
                _cont.active = data.active
            if data.description:
                _cont.description = data.description
            if data.video:
                _cont.video = data.video
            if data.image:
                _cont.image = data.image
            if (
                data.chapter is not None
                and data.order is not None
                and (
                    int(data.chapter) is not int(_cont.chapter)
                    or int(data.order) is not int(_cont.order)
                )
            ):
                if (
                    self.session.query(CourseDTO)
                    .filter_by(id=course_id)
                    .one()
                    .has_content_with_chapter(data.chapter, data.order)
                ):
                    raise ChapterAlreadyInCourseError
                _cont.chapter = data.chapter
                _cont.order = data.order
        except:
            raise

        return _cont.to_read_model()

    def user_involved(self, course_id: str, user_id: str) -> bool:
        course = self.session.query(CourseDTO).filter_by(id=course_id).first()
        if course is None:
            raise CourseNotFoundError
        return course.has_active_collab_with_id(user_id) or course.creator_id == user_id

    def add_review(self, review: Review):
        try:
            course: CourseDTO = (
                self.session.query(CourseDTO).filter_by(id=review.course_id).first()
            )
            if course.has_review_from_user(review.id):
                raise UserAlreadyReviewedCourseError
            r = ReviewDTO.from_entity(review)
            course.reviews.append(r)
        except NoResultFound:
            raise CourseNotFoundError
        return r.to_read_model()


class CourseCommandUseCaseUnitOfWorkImpl(CourseCommandUseCaseUnitOfWork):
    def __init__(
        self,
        session: Session,
        course_repository: CourseRepository,
    ):
        self.session: Session = session
        self.course_repository: CourseRepository = course_repository

    def begin(self):
        self.session.begin()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
