from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.card import Card
from app.models.sale import Sale
from app.providers.sales.base import NormalizedSale
from app.services.fx import to_usd


async def upsert_sales(db: AsyncSession, card_id: int, sales: list[NormalizedSale]) -> None:
    for s in sales:
        price_usd = await to_usd(s.price, s.currency)
        shipping_usd = await to_usd(s.shipping, s.currency) if s.shipping is not None else None

        stmt = (
            insert(Sale)
            .values(
                card_id=card_id,
                provider=s.provider,
                source_sale_id=s.source_sale_id,
                title=s.title,
                price=price_usd,
                currency="USD",
                original_price=s.price,
                original_currency=s.currency,
                shipping=shipping_usd,
                condition=s.condition,
                grading_company=s.grading_company,
                grade=s.grade,
                listing_type=s.listing_type,
                sold_at=s.sold_at,
                listing_url=s.listing_url,
            )
            .on_conflict_do_nothing(index_elements=["provider", "source_sale_id"])
        )
        await db.execute(stmt)
    await db.commit()


async def list_sales(db: AsyncSession, card_id: int, limit: int = 100) -> list[Sale]:
    result = await db.execute(
        select(Sale).where(Sale.card_id == card_id).order_by(Sale.sold_at.desc()).limit(limit)
    )
    return list(result.scalars().all())


async def list_recent_sales(db: AsyncSession, limit: int = 50) -> list[tuple[Sale, Card]]:
    result = await db.execute(
        select(Sale, Card)
        .join(Card, Card.id == Sale.card_id)
        .order_by(Sale.sold_at.desc())
        .limit(limit)
    )
    return [(row[0], row[1]) for row in result.all()]
