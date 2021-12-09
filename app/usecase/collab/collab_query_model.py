from typing import List

from pydantic import BaseModel, Field


class UserReadModel(BaseModel):

    id: str = Field(example="Kgj1yXyrZ4NBeplhONPJ4xeLuQv2")
    username: str = Field(example="jany99")
    name: str = Field(example="Jane")
    active: bool = Field(example=True)
    lastName: str = Field(example="Doe")
    role: int = Field(example=1)
    dateOfBirth: str = Field(example="Wed Nov 10 2021")
    country: str = Field(example="Argentina")
    language: str = Field(example="Spanish")
    mail: str = Field(example="jane@doe.com")

    class Config:
        orm_mode = True


class CollabReadModel(BaseModel):

    id: str = Field(example="user_0")
    course_id: str = Field(example="course_0")
    active: bool = Field(example=True)

    class Config:
        orm_mode = True

    def get_id(self):
        return self.id


class PaginatedUserReadModel(BaseModel):
    users: List[UserReadModel] = Field(example=UserReadModel.schema())
    count: int = Field(ge=0, example=1)
