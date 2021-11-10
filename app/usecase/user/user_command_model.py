from pydantic import BaseModel, Field


class UserCreateModel(BaseModel):

    id: str = Field(example="user_0")
    role: str = Field(example="student")

    class Config:
        orm_mode = True

    def is_student(self):
        return self.role == "student"

    def is_colab(self):
        return self.role == "colab"
