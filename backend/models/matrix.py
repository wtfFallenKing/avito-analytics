from enum import Enum

from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.engine import Base


class MatrixTypeEnum(Enum):
    BASE = "BASE"
    DISCOUNT = "DISCOUNT"


class Matrix(Base):
    __tablename__ = "matrices"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    segment_id: Mapped[int] = mapped_column(nullable=True)
    type: Mapped[ENUM] = mapped_column(
        ENUM(MatrixTypeEnum, name="matrix_type_enum", create_type=True),
        nullable=False,
        default=MatrixTypeEnum.BASE,
    )

    prices = relationship("Price", back_populates="matrix")
