from datetime import datetime
from typing import List, Union

import shortuuid
from sqlalchemy import BigInteger, Boolean, Column, Float, ForeignKey, String, Text
from sqlalchemy.orm import relationship

from app.domain.course import Course
from app.infrastructure.database import Base
from app.usecase.collab.collab_query_model import CollabReadModel
from app.usecase.content.content_command_model import ContentCreateModel
from app.usecase.content.content_query_model import ContentReadModel
from app.usecase.course import CourseReadModel


def unixtimestamp() -> int:
    return int(datetime.now().timestamp() * 1000)


def get_categories(categories):
    v = []
    for i in categories:
        v.append(i.category)
    return v


def create_categories(id, categories):
    v = []
    if categories is None:
        return v
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
    presentation_video: Union[str, Column] = Column(
        String, nullable=False, autoincrement=False
    )
    image: Union[str, Column] = Column(String, nullable=False, autoincrement=False)
    created_at: Union[int, Column] = Column(BigInteger, index=True, nullable=False)
    updated_at: Union[int, Column] = Column(BigInteger, index=True, nullable=False)

    categories = relationship("Category", cascade="all, delete")
    collabs = relationship("Collab", cascade="all, delete")
    content = relationship("Content", cascade="all, delete")

    def to_entity(self) -> Course:
        return Course(
            id=self.id,
            creator_id=self.creator_id,
            name=self.name,
            price=self.price,
            language=self.language,
            description=self.description,
            categories=get_categories(self.categories),
            presentation_video=self.presentation_video,
            image=self.image,
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
            presentation_video=self.presentation_video,
            image=self.image,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def has_active_collab_with_id(self, id: str):
        return (
            len(list(filter(lambda c: c.active and c.user_id == id, self.collabs))) > 0
        )

    def has_content_with_chapter(self, chapter: int):
        for i in self.content:
            if int(i.chapter) == chapter:
                return True
        return False

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
            presentation_video=course.presentation_video,
            image=course.image,
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


class Collab(Base):

    __tablename__ = "collabs"
    id: Union[str, Column] = Column(String, primary_key=True, autoincrement=False)
    user_id: Union[str, Column] = Column(String, nullable=False, autoincrement=False)
    course_id: Union[str, Column] = Column(
        String, ForeignKey("courses.id"), autoincrement=False
    )
    active: Union[bool, Column] = Column(Boolean, nullable=False, autoincrement=False)

    def to_read_model(self) -> CollabReadModel:
        return CollabReadModel(
            id=self.user_id,
            course_id=self.course_id,
        )

    def deactivate(self):
        self.active = False

    @staticmethod
    def from_read_model(user: CollabReadModel) -> "Collab":
        return Collab(
            id=shortuuid.uuid(),
            user_id=user.id,
            course_id=user.course_id,
            active=user.active,
        )


class Content(Base):

    __tablename__ = "content"
    id: Union[str, Column] = Column(String, primary_key=True, autoincrement=False)
    title: Union[str, Column] = Column(String, nullable=False, autoincrement=False)
    course_id: Union[str, Column] = Column(
        String, ForeignKey("courses.id"), autoincrement=False
    )
    chapter: Union[str, Column] = Column(String, nullable=False, autoincrement=False)
    description: Union[str, Column] = Column(Text, nullable=False, autoincrement=False)
    video: Union[str, Column] = Column(String, nullable=False, autoincrement=False)
    image: Union[str, Column] = Column(String, nullable=False, autoincrement=False)
    active: Union[bool, Column] = Column(Boolean, nullable=False, autoincrement=False)

    @staticmethod
    def from_create_model(
        id: str, content: ContentCreateModel, course_id: str
    ) -> "Content":
        return Content(
            id=id,
            title=content.title,
            course_id=course_id,
            chapter=content.chapter,
            description=content.description,
            video=content.video,
            image=content.image,
            active=True,
        )

    def to_read_model(self):
        return ContentReadModel(
            id=self.id,
            title=self.title,
            chapter=self.chapter,
            description=self.description,
            video=self.video,
            image=self.image,
        )
