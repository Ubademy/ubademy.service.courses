from datetime import datetime
from typing import List, Union

import shortuuid
from sqlalchemy import BigInteger, Column, Float, ForeignKey, String, Text
from sqlalchemy.orm import relationship

from app.domain.course import Course
from app.infrastructure.sqlite.database import Base
from app.usecase.course import CourseReadModel
from app.usecase.user.user_query_model import UserReadModel


def unixtimestamp() -> int:
    return int(datetime.now().timestamp() * 1000)


def get_categories(categories):
    v = []
    for i in categories:
        v.append(i.category)
    return v


def create_categories(id, categories):
    v = []
    for i in categories:
        v.append(Category(id=shortuuid.uuid(), course_id=id, category=i))
    return v


class CourseDTO(Base):

    __tablename__ = "courses"
    id: Union[str, Column] = Column(String, primary_key=True, autoincrement=False)
    creator_id: Union[str, Column] = Column(String, autoincrement=False)
    name: Union[str, Column] = Column(String, nullable=False, autoincrement=False)
    price: Union[float, Column] = Column(Float, nullable=False)
    language: Union[str, Column] = Column(String, nullable=False, autoincrement=False)
    description: Union[str, Column] = Column(Text, nullable=False, autoincrement=False)
    created_at: Union[int, Column] = Column(BigInteger, index=True, nullable=False)
    updated_at: Union[int, Column] = Column(BigInteger, index=True, nullable=False)

    categories = relationship("Category", cascade="all, delete")
    users = relationship("User", cascade="all, delete")

    def to_entity(self) -> Course:
        return Course(
            id=self.id,
            creator_id=self.creator_id,
            name=self.name,
            price=self.price,
            language=self.language,
            description=self.description,
            categories=get_categories(self.categories),
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
            categories=get_categories(self.categories),
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
            categories=create_categories(course.id, course.categories),
            created_at=course.created_at,
            updated_at=now,
        )

    def get_categories(self) -> List[str]:
        return get_categories(self.categories)


class Category(Base):

    __tablename__ = "categories"
    id: Union[str, Column] = Column(String, primary_key=True, autoincrement=False)
    course_id: Union[str, Column] = Column(
        String, ForeignKey("courses.id"), autoincrement=False
    )
    category: Union[str, Column] = Column(String, nullable=False, autoincrement=False)


class User(Base):

    __tablename__ = "users"
    id: Union[str, Column] = Column(String, primary_key=True, autoincrement=False)
    user_id: Union[str, Column] = Column(String, nullable=False, autoincrement=False)
    course_id: Union[str, Column] = Column(
        String, ForeignKey("courses.id"), autoincrement=False
    )
    role: Union[str, Column] = Column(String, nullable=False, autoincrement=False)

    def to_read_model(self) -> UserReadModel:
        return UserReadModel(
            id=self.user_id,
            course_id=self.course_id,
            role=self.role,
        )

    @staticmethod
    def from_read_model(user: UserReadModel) -> "User":
        return User(
            id=shortuuid.uuid(),
            user_id=user.id,
            course_id=user.course_id,
            role=user.role,
        )
