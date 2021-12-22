from typing import List

from pydantic import BaseModel, Field


class SubscriptionMetricsReadModel(BaseModel):

    subscriptions: List[int] = Field(example=[14, 9, 2])
