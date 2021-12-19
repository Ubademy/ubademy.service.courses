from typing import List

from pydantic import BaseModel, Field


class NewCoursesMetricsReadModel(BaseModel):

    year: int = Field(default=0, example=2021)
    months: List[int] = Field(example=[0] * 12)
