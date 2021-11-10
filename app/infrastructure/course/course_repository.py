from typing import Optional

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from app.domain.course import Course, CourseNotFoundError, CourseRepository
from app.domain.user.user_exception import UserAlreadyInCourseError
from app.usecase.course import CourseCommandUseCaseUnitOfWork
from app.usecase.user.user_query_model import UserReadModel

from ...usecase.user.user_command_model import UserCreateModel
from .course_dto import Category, CourseDTO, User


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
    ) -> Optional[UserReadModel]:
        try:
            course = self.session.query(CourseDTO).filter_by(id=course_id).first()
            if course.has_active_user_with_id(data.id):
                raise UserAlreadyInCourseError
            user = UserReadModel(id=data.id, course_id=course_id, role=data.role)
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
