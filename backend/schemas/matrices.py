from enum import Enum
from typing import Optional

from pydantic import BaseModel


class MatrixTypePydantic(str, Enum):
    BASE = "BASE"
    DISCOUNT = "DISCOUNT"


class MatrixCreateRequest(BaseModel):
    name: str
    type: MatrixTypePydantic = MatrixTypePydantic.BASE
    segment_id: Optional[int]


class MatrixPutRequest(BaseModel):
    name: str
    segment_id: Optional[int] = None


class MatrixResponse(BaseModel):
    id: int
    name: str
    type: MatrixTypePydantic
    segment_id: Optional[int]
