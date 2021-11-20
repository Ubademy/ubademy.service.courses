from typing import List

from pydantic import BaseModel, Field


class UserReadModel(BaseModel):

    id: str = Field(example="Kgj1yXyrZ4NBeplhONPJ4xeLuQv2")
    username: str = Field(example="jany99")
    name: str = Field(example="Jane")
    lastName: str = Field(example="Doe")
    active: bool = Field(example=True)
    role: int = Field(example=1)
    dateOfBirth: str = Field(example="Wed Nov 10 2021")
    country: str = Field(example="Argentina")
    language: str = Field(example="Spanish")
    mail: str = Field(example="jane@doe.com")

    class Config:
        orm_mode = True


class MiniUserReadModel(BaseModel):

    id: str = Field(example="user_0")
    course_id: str = Field(example="course_0")
    role: str = Field(example="student")

    class Config:
        orm_mode = True

    def is_student(self):
        return self.role == "student"

    def is_colab(self):
        return self.role == "colab"

    def get_id(self):
        return self.id


class PaginatedUserReadModel(BaseModel):
    users: List[UserReadModel] = Field(example=UserReadModel.schema())
    count: int = Field(ge=0, example=1)
