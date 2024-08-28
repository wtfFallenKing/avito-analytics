from datetime import datetime
from enum import Enum

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column

from models.engine import Base


class MatrixLogsTypeEnum(Enum):
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"


class MatrixLogs(Base):
    __tablename__ = "matrix_logs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    matrix_id: Mapped[int] = mapped_column(
        ForeignKey("matrices.id", ondelete="SET NULL"), primary_key=False, nullable=True
    )
    happened_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    type: Mapped[ENUM] = mapped_column(
        ENUM(MatrixLogsTypeEnum, name="matrix_logs_type_enum", create_type=True),
        nullable=False,
        default=MatrixLogsTypeEnum.CREATE,
    )
