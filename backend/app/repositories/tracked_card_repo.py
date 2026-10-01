from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tracked_card import TrackedCard

CACHE_TTL_HOURS = 6


async def needs_refresh(db: AsyncSession, card_id: int) -> bool:
    result = await db.execute(select(TrackedCard).where(TrackedCard.card_id == card_id))
    tracked = result.scalar_one_or_none()
    if tracked is None:
        db.add(TrackedCard(card_id=card_id, active=True))
        await db.commit()
        return True

    if tracked.last_checked_at is None:
        return True
    return datetime.now(timezone.utc) - tracked.last_checked_at > timedelta(hours=CACHE_TTL_HOURS)


async def mark_checked(db: AsyncSession, card_id: int) -> None:
    result = await db.execute(select(TrackedCard).where(TrackedCard.card_id == card_id))
    tracked = result.scalar_one_or_none()
    if tracked:
        tracked.last_checked_at = datetime.now(timezone.utc)
        await db.commit()
