from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, Integer, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class PriceSnapshot(Base):
    __tablename__ = "price_snapshots"
    __table_args__ = (Index("ix_price_snapshots_card_id", "card_id"),)
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    card_id: Mapped[int] = mapped_column(ForeignKey("cards.id"))
    calculated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    latest_sale: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    average_price: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    median_price: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    min_price: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    max_price: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    sales_count: Mapped[int] = mapped_column(Integer, default=0)
