from typing import List, Optional, Tuple

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from app.domain.collab.collab_exception import NoCollabsInCourseError
from app.usecase.collab.collab_query_model import CollabReadModel
from app.usecase.course import CourseQueryService, CourseReadModel

from ...domain.course import CourseNotFoundError
from ...usecase.content.content_query_model import ContentReadModel
from .course_dto import Category, CourseDTO


class CourseQueryServiceImpl(CourseQueryService):
    def __init__(self, session: Session):
        self.session: Session = session

    def find_by_id(self, id: str) -> Optional[CourseReadModel]:
        try:
            course_dto = self.session.query(CourseDTO).filter_by(id=id).one()
        except NoResultFound:
            return None
        except:
            raise

        return course_dto.to_read_model()

    def find_all(
        self, limit: int = 100, offset: int = 0
    ) -> Tuple[List[CourseReadModel], int]:
        try:
            course_dtos = (
                self.session.query(CourseDTO)
                .order_by(CourseDTO.updated_at)
                .slice(limit * offset, limit * (offset + 1))
                .all()
            )
        except:
            raise

        return (
            list(map(lambda course_dto: course_dto.to_read_model(), course_dtos)),
            self.session.query(CourseDTO).count(),
        )

    def find_all_categories(self) -> List[str]:
        try:
            categories = self.session.query(Category).limit(100).all()
        except:
            raise

        return list(dict.fromkeys(list(map(lambda cat: cat.category, categories))))

    def find_by_filters(
        self,
        ids: Optional[List[str]],
        name: Optional[str],
        creator_id: Optional[str],
        colab_id: Optional[str],
        inactive: Optional[bool],
        category: Optional[str],
        language: Optional[str],
        ignore_free: Optional[bool],
        ignore_paid: Optional[bool],
        text: Optional[str],
        limit: int = 100,
        offset: int = 0,
    ) -> Tuple[List[CourseReadModel], int]:
        try:
            courses_q = self.session.query(CourseDTO)
            if ids:
                courses_q = courses_q.filter(CourseDTO.id.in_(ids))  # type: ignore
            if name:
                courses_q = courses_q.filter_by(name=name)
            if creator_id:
                courses_q = courses_q.filter_by(creator_id=creator_id)
            if colab_id:
                courses_q = courses_q.filter(
                    CourseDTO.users.any(user_id=colab_id, role="colab")
                )
            if colab_id and not inactive:
                courses_q = courses_q.filter(
                    CourseDTO.users.any(user_id=colab_id, role="colab", active=True)
                )
            if language:
                courses_q = courses_q.filter_by(language=language)
            if ignore_free:
                courses_q = courses_q.filter(CourseDTO.price > 0)
            if ignore_paid:
                courses_q = courses_q.filter(CourseDTO.price == 0)
            if category:
                courses_q = courses_q.filter(
                    CourseDTO.categories.any(category=category)
                )
            if text:
                text = "%" + text + "%"
                courses_q = courses_q.filter(
                    (CourseDTO.name.ilike(text))  # type: ignore
                    | (CourseDTO.description.ilike(text))  # type: ignore
                )

            course_dtos = courses_q.slice(limit * offset, limit * (offset + 1)).all()
        except:
            raise

        return (
            list(map(lambda course_dto: course_dto.to_read_model(), course_dtos)),
            courses_q.count(),
        )

    def find_collabs_by_id(self, id: str) -> List[CollabReadModel]:
        try:
            course = self.session.query(CourseDTO).filter_by(id=id).first()
            if not course:
                raise CourseNotFoundError
            collabs = list(filter(lambda c: c.active, course.collabs))
            if len(collabs) == 0:
                raise NoCollabsInCourseError
        except:
            raise

        return list(map(lambda collab: collab.to_read_model(), collabs))

    def fetch_content_by_id(self, id: str) -> List[ContentReadModel]:
        try:
            course = self.session.query(CourseDTO).filter_by(id=id).first()
            if not course:
                raise CourseNotFoundError
            content = list(filter(lambda c: c.active, course.content))

        except:
            raise

        return list(map(lambda c: c.to_read_model(), content))
