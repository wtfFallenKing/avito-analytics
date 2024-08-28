from typing import Optional

from pydantic import BaseModel


class LocationCreateRequest(BaseModel):
    id: int
    name: str
    parent_id: Optional[int]


class LocationPutRequest(BaseModel):
    key: str
    name: str


class LocationResponse(BaseModel):
    id: int
    key: str
    name: str
    parent_id: Optional[int]
