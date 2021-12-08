from datetime import datetime
from typing import List, Union

import shortuuid
from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app.domain.course import Course
from app.domain.review.review import Review
from app.infrastructure.database import Base
from app.usecase.collab.collab_query_model import CollabReadModel
from app.usecase.content.content_command_model import ContentCreateModel
from app.usecase.content.content_query_model import ContentReadModel
from app.usecase.course import CourseReadModel
from app.usecase.review.review_query_model import ReviewReadModel


def unixtimestamp() -> int:
    return int(datetime.now().timestamp() * 1000)


def get_categories(categories):
    v = []
    for i in categories:
        v.append(i.category)
    return v


def get_recommendations(reviews):
    return {
        "recommended": len(list(filter(lambda x: x.is_recommended(), reviews))),
        "total": len(reviews),
    }


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
    subscription_id: Union[int, Column] = Column(Integer, nullable=False)
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
    reviews = relationship("ReviewDTO", cascade="all, delete")

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
            subscription_id=self.subscription_id,
            recommendations=get_recommendations(self.reviews),
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def to_read_model(self) -> CourseReadModel:
        return CourseReadModel(
            id=self.id,
            creator_id=self.creator_id,
            name=self.name,
            price=self.price,
            subscription_id=self.subscription_id,
            language=self.language,
            description=self.description,
            categories=get_categories(self.categories),
            recommendations=get_recommendations(self.reviews),
            presentation_video=self.presentation_video,
            image=self.image,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def has_active_collab_with_id(self, id: str):
        return (
            len(list(filter(lambda c: c.active and c.user_id == id, self.collabs))) > 0
        )

    def has_content_with_chapter(self, chapter: int, order: int):
        for i in self.content:
            if int(i.chapter) == chapter and int(i.order) == order:
                return True
        return False

    def has_review_from_user(self, id: str):
        return len(list(filter(lambda r: r.id == id, self.reviews))) > 0

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
            subscription_id=course.subscription_id,
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
    chapter_title: Union[str, Column] = Column(
        String, nullable=False, autoincrement=False
    )
    subtitle: Union[str, Column] = Column(String, nullable=False, autoincrement=False)
    course_id: Union[str, Column] = Column(
        String, ForeignKey("courses.id"), autoincrement=False
    )
    chapter: Union[str, Column] = Column(String, nullable=False, autoincrement=False)
    order: Union[str, Column] = Column(String, nullable=False, autoincrement=False)
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
            chapter_title=content.chapter_title,
            subtitle=content.subtitle,
            course_id=course_id,
            chapter=content.chapter,
            order=content.order,
            description=content.description,
            video=content.video,
            image=content.image,
            active=True,
        )

    def to_read_model(self):
        return ContentReadModel(
            id=self.id,
            chapter_title=self.chapter_title,
            subtitle=self.subtitle,
            chapter=self.chapter,
            order=self.order,
            description=self.description,
            video=self.video,
            image=self.image,
        )


class ReviewDTO(Base):
    __tablename__ = "reviews"
    id: Union[str, Column] = Column(String, primary_key=True, autoincrement=False)
    course_id: Union[str, Column] = Column(
        String, ForeignKey("courses.id"), primary_key=True, autoincrement=False
    )
    recommended: Union[bool, Column] = Column(
        Boolean, nullable=False, autoincrement=False
    )
    review: Union[str, Column] = Column(Text, nullable=False, autoincrement=False)
    date: Union[int, Column] = Column(BigInteger, index=True, nullable=False)

    @staticmethod
    def from_entity(r: Review):
        now = unixtimestamp()
        return ReviewDTO(
            id=r.id,
            course_id=r.course_id,
            recommended=r.recommended,
            review=r.review,
            date=now,
        )

    def to_read_model(self):
        return ReviewReadModel(
            id=self.id,
            course_id=self.course_id,
            recommended=self.recommended,
            review=self.review,
            date=self.date,
        )

    def is_recommended(self):
        return self.recommended
