from datetime import datetime
from typing import Union

from sqlalchemy import Column, Integer, String, BigInteger

from app.domain.course import Course
from app.infrastructure.sqlite.database import Base
from app.usecase.course import CourseReadModel


def unixtimestamp() -> int:
    return int(datetime.now().timestamp() * 1000)


class CourseDTO(Base):

    __tablename__ = "courses"
    id: Union[str, Column] = Column(String, primary_key=True, autoincrement=False)
    name: Union[str, Column] = Column(String, nullable=False, autoincrement=False)
    categories: Union[str, Column] = Column(String, nullable=False, autoincrement=False)
    price: Union[int, Column] = Column(Integer, nullable=False)
    created_at: Union[int, Column] = Column(BigInteger, index=True, nullable=False)
    updated_at: Union[int, Column] = Column(BigInteger, index=True, nullable=False)

    def to_entity(self) -> Course:
        return Course(
            id=self.id,
            name=self.name,
            categories=self.categories,
            price=self.price,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def to_read_model(self) -> CourseReadModel:
        return CourseReadModel(
            id=self.id,
            name=self.name,
            categories=self.categories,
            price=self.price,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @staticmethod
    def from_entity(course: Course) -> "CourseDTO":
        now = unixtimestamp()
        return CourseDTO(
            id=course.id,
            name=course.name,
            categories=course.categories,
            price=course.price,
            created_at=now,
            updated_at=now,
        )
