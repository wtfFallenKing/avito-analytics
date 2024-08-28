from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class MatrixLogTypePydantic(str, Enum):
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"


class MatrixLogResponse(BaseModel):
    id: int
    matrix_id: Optional[int]
    type: MatrixLogTypePydantic
    happened_at: datetime
