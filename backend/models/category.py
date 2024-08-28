from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.engine import Base


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column()

    parent_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("categories.id", ondelete="cascade"), nullable=True
    )
    prices = relationship("Price", back_populates="category")
