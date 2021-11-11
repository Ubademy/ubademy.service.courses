from typing import Optional

import shortuuid
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from app.domain.course import Course, CourseNotFoundError, CourseRepository
from app.domain.user.user_exception import UserAlreadyInCourseError
from app.usecase.course import CourseCommandUseCaseUnitOfWork
from app.usecase.user.user_query_model import MiniUserReadModel

from ...domain.user.content.content_exception import ChapterAlreadyInCourseError
from ...usecase.content.content_command_model import ContentCreateModel
from ...usecase.content.content_query_model import ContentReadModel
from ...usecase.user.user_command_model import UserCreateModel
from .course_dto import Category, Content, CourseDTO, User


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
            _course = self.session.query(CourseDTO).filter_by(id=course_dto.id).one()
            if course_dto.name:
                _course.name = course_dto.name
            if course_dto.language:
                _course.language = course_dto.language
            if course_dto.price is not None:
                _course.price = course_dto.price
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

    def add_user(
        self, data: UserCreateModel, course_id: str
    ) -> Optional[MiniUserReadModel]:
        try:
            course = self.session.query(CourseDTO).filter_by(id=course_id).first()
            if course.has_active_user_with_id(data.id):
                raise UserAlreadyInCourseError
            user = MiniUserReadModel(id=data.id, course_id=course_id, role=data.role)
            course.users.append(User.from_read_model(user))
        except NoResultFound:
            raise CourseNotFoundError
        except:
            raise
        return user

    def deactivate_user_from_course(self, user_id, course_id):
        try:
            users = (
                self.session.query(User)
                .filter_by(user_id=user_id, course_id=course_id)
                .all()
            )
            for i in users:
                i.deactivate()
        except:
            raise

    def add_content(
        self, data: ContentCreateModel, course_id: str
    ) -> Optional[ContentReadModel]:
        try:
            uuid = shortuuid.uuid()
            course = self.session.query(CourseDTO).filter_by(id=course_id).first()
            if course.has_content_with_chapter(data.chapter):
                raise ChapterAlreadyInCourseError
            content = Content.from_create_model(
                id=uuid, content=data, course_id=course_id
            )
            course.content.append(content)
        except NoResultFound:
            raise CourseNotFoundError
        except:
            raise
        return content.to_read_model()


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
