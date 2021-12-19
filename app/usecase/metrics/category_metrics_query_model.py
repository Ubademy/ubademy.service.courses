from typing import List

from pydantic import BaseModel, Field


class CategoryMetricsReadModel(BaseModel):

    category: str = Field(example="Programming")
    count: int = Field(example=10)


class PaginatedCategoryMetricsReadModel(BaseModel):

    categories: List[CategoryMetricsReadModel] = Field(
        example=[CategoryMetricsReadModel.schema()]
    )
    count: int = Field(example=10)
