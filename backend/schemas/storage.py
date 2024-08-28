from datetime import datetime
from typing import List

from pydantic import BaseModel


class StorageConfResponse(BaseModel):
    baseline: int
    discounts: List[int]


class StorageLogsResponse(BaseModel):
    id: int
    baseline: int
    discounts: List[int]
    happened_at: datetime


class SetDiscountsRequest(BaseModel):
    discounts: List[int]
