from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.card import Card
from app.models.sale import Sale
from app.providers.cards.base import NormalizedCard


async def upsert_card(db: AsyncSession, normalized: NormalizedCard) -> Card:
    result = await db.execute(select(Card).where(Card.external_id == normalized.external_id))
    card = result.scalar_one_or_none()
    if card is None:
        card = Card(external_id=normalized.external_id)
        db.add(card)

    card.name = normalized.name
    card.set_id = normalized.set_id
    card.set_name = normalized.set_name
    card.card_number = normalized.card_number
    card.rarity = normalized.rarity
    card.supertype = normalized.supertype
    card.subtypes = ",".join(normalized.subtypes) if normalized.subtypes else None
    card.image_small = normalized.image_small
    card.image_large = normalized.image_large
    card.language = normalized.language

    await db.flush()
    return card


async def get_card(db: AsyncSession, card_id: int) -> Card | None:
    return await db.get(Card, card_id)


async def get_top_cards(db: AsyncSession, limit: int = 12) -> list[tuple[Card, int]]:
    result = await db.execute(
        select(Card, func.count(Sale.id).label("sales_count"))
        .join(Sale, Sale.card_id == Card.id)
        .group_by(Card.id)
        .order_by(func.count(Sale.id).desc())
        .limit(limit)
    )
    return [(row[0], row[1]) for row in result.all()]


async def get_all_cards(db: AsyncSession, limit: int = 200, offset: int = 0) -> list[tuple[Card, int]]:
    result = await db.execute(
        select(Card, func.count(Sale.id).label("sales_count"))
        .outerjoin(Sale, Sale.card_id == Card.id)
        .group_by(Card.id)
        .order_by(Card.name)
        .limit(limit)
        .offset(offset)
    )
    return [(row[0], row[1]) for row in result.all()]
