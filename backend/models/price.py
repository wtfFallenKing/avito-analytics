from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.engine import Base
from models.matrix import Matrix
from models.location import Location
from models.category import Category


class Price(Base):
    __tablename__ = "prices"

    price: Mapped[int] = mapped_column()

    matrix_id: Mapped[int] = mapped_column(ForeignKey("matrices.id", ondelete="cascade"), primary_key=True)
    matrix: Mapped[Matrix] = relationship(back_populates="prices")

    location_id: Mapped[int] = mapped_column(ForeignKey("locations.id", ondelete="cascade"), primary_key=True)
    location: Mapped[Location] = relationship(back_populates="prices")

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="cascade"), primary_key=True
    )
    category: Mapped[Category] = relationship(back_populates="prices")
