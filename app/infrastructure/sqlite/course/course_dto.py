from datetime import datetime
from typing import Union, List

from sqlalchemy import Column, String, BigInteger, Float, Text

from app.domain.course import Course
from app.infrastructure.sqlite.database import Base
from app.usecase.course import CourseReadModel


def unixtimestamp() -> int:
    return int(datetime.now().timestamp() * 1000)


class CourseDTO(Base):

    __tablename__ = "courses"
    id: Union[str, Column] = Column(String, primary_key=True, autoincrement=False)
    creator_id: Union[str, Column] = Column(String, primary_key=True, autoincrement=False)
    name: Union[str, Column] = Column(String, nullable=False, autoincrement=False)
    price: Union[float, Column] = Column(Float, nullable=False)
    language: Union[str, Column] = Column(String, nullable=False, autoincrement=False)
    description: Union[str, Column] = Column(Text, nullable=False, autoincrement=False)
    created_at: Union[int, Column] = Column(BigInteger, index=True, nullable=False)
    updated_at: Union[int, Column] = Column(BigInteger, index=True, nullable=False)


    def to_entity(self) -> Course:
        return Course(
            id=self.id,
            creator_id=self.creator_id,
            name=self.name,
            price=self.price,
            language=self.language,
            description=self.description,
            categories=[],
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def to_read_model(self) -> CourseReadModel:
        return CourseReadModel(
            id=self.id,
            creator_id=self.creator_id,
            name=self.name,
            price=self.price,
            language=self.language,
            description=self.description,
            categories=[],
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @staticmethod
    def from_entity(course: Course) -> "CourseDTO":
        now = unixtimestamp()
        if course.created_at is None:
            course.created_at = now
        return CourseDTO(
            id=course.id,
            creator_id=course.creator_id,
            name=course.name,
            price=course.price,
            language=course.language,
            description=course.description,
            created_at=course.created_at,
            updated_at=now,
        )
