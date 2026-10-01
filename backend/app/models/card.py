from datetime import datetime

from sqlalchemy import DateTime, Index, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Card(Base):
    __tablename__ = "cards"
    __table_args__ = (
        Index("ix_cards_name", "name"),
        Index("ix_cards_card_number", "card_number"),
        Index("ix_cards_set_id", "set_id"),
    )
    # without this, accessing updated_at (onupdate=func.now()) after commit triggers
    # an implicit lazy-reload outside the async greenlet context -> MissingGreenlet error.
    # eager_defaults fetches server-computed columns via RETURNING during flush instead.
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    external_id: Mapped[str] = mapped_column(String, unique=True, index=True)
    name: Mapped[str] = mapped_column(String)
    set_id: Mapped[str] = mapped_column(String)
    set_name: Mapped[str] = mapped_column(String)
    card_number: Mapped[str] = mapped_column(String)
    rarity: Mapped[str | None] = mapped_column(String, nullable=True)
    supertype: Mapped[str | None] = mapped_column(String, nullable=True)
    subtypes: Mapped[str | None] = mapped_column(String, nullable=True)  # comma-joined, e.g. "Stage 2,ex"
    image_small: Mapped[str | None] = mapped_column(String, nullable=True)
    image_large: Mapped[str | None] = mapped_column(String, nullable=True)
    language: Mapped[str] = mapped_column(String, default="EN")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
