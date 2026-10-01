from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, Numeric, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Sale(Base):
    __tablename__ = "sales"
    __table_args__ = (
        UniqueConstraint("provider", "source_sale_id", name="uq_sales_provider_source_sale_id"),
        Index("ix_sales_card_id", "card_id"),
        Index("ix_sales_sold_at", "sold_at"),
        Index("ix_sales_provider", "provider"),
    )
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    card_id: Mapped[int] = mapped_column(ForeignKey("cards.id"))
    provider: Mapped[str] = mapped_column(String)
    source_sale_id: Mapped[str | None] = mapped_column(String, nullable=True)
    title: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column(Numeric(10, 2))  # always USD
    currency: Mapped[str] = mapped_column(String)  # always "USD"; kept for schema stability
    original_price: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    original_currency: Mapped[str | None] = mapped_column(String, nullable=True)
    shipping: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    condition: Mapped[str | None] = mapped_column(String, nullable=True)
    grading_company: Mapped[str | None] = mapped_column(String, nullable=True)
    grade: Mapped[str | None] = mapped_column(String, nullable=True)
    listing_type: Mapped[str | None] = mapped_column(String, nullable=True)
    sold_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    listing_url: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
