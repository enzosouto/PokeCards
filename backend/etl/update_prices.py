"""Recompute and persist a price snapshot for every card that has sales.

Run with: python -m etl.update_prices
"""

import asyncio

from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.price_snapshot import PriceSnapshot
from app.models.sale import Sale
from app.repositories.stats_repo import compute_stats


async def main():
    async with SessionLocal() as db:
        card_ids = (await db.execute(select(Sale.card_id).distinct())).scalars().all()

        for card_id in card_ids:
            stats = await compute_stats(db, card_id)
            db.add(
                PriceSnapshot(
                    card_id=card_id,
                    latest_sale=stats.latest_sale,
                    average_price=stats.average,
                    median_price=stats.median,
                    min_price=stats.minimum,
                    max_price=stats.maximum,
                    sales_count=stats.count,
                )
            )
            print(f"[ok] card={card_id}: snapshot saved (count={stats.count})")

        await db.commit()


if __name__ == "__main__":
    asyncio.run(main())
