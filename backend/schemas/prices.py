from typing import Optional

from pydantic import BaseModel


class PriceReadRequest(BaseModel):
    matrix_id: Optional[int]
    location_id: Optional[int]
    category_id: Optional[int]


class PriceCreateRequest(BaseModel):
    price: int
    matrix_id: int
    location_id: int
    category_id: int


class PriceGetRequest(BaseModel):
    location_id: int
    category_id: int
    user_id: int


class PricePutRequest(BaseModel):
    price: int
    matrix_id: int
    location_id: int
    category_id: int


class PriceResponse(BaseModel):
    price: int
    matrix_id: int
    location_id: int
    category_id: int


class PriceGetResponse(BaseModel):
    price: float
    location_id: int
    category_id: int
    matrix_id: int
    segment_id: Optional[int] = None
