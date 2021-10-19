from typing import Optional

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from app.domain.course import Course, CourseRepository
from app.usecase.course import CourseCommandUseCaseUnitOfWork

from .course_dto import CourseDTO


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
            return None

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
            _course.name = course_dto.name
            _course.categories = course_dto.categories
            _course.price = course_dto.price
        except:
            raise

    def delete_by_id(self, id: str):
        try:
            self.session.query(CourseDTO).filter_by(id=id).delete()
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
