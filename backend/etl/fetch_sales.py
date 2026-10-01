"""Fetch recent sales for all actively tracked cards and persist them.

Run with: python -m etl.fetch_sales
"""

import asyncio
import sys

from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.card import Card
from app.models.tracked_card import TrackedCard
from app.providers.sales.base import NormalizedSale
from app.repositories.sale_repo import upsert_sales
from app.repositories.tracked_card_repo import mark_checked, needs_refresh
from app.services.sales_fetch import fetch_sales_from_providers

SUSPICIOUS_WORDS = {"proxy", "custom", "fake", "reprint", "lot", "replica"}


def validate_sale(sale: NormalizedSale) -> str | None:
    """Returns a rejection reason, or None if the sale is valid."""
    if sale.price <= 0:
        return f"price <= 0 ({sale.price})"
    if not sale.currency:
        return "missing currency"
    lowered = sale.title.lower()
    hit = next((w for w in SUSPICIOUS_WORDS if w in lowered), None)
    if hit:
        return f"suspicious keyword '{hit}' in title"
    return None


async def main():
    sys.stdout.reconfigure(errors="replace")
    async with SessionLocal() as db:
        result = await db.execute(
            select(TrackedCard, Card)
            .join(Card, Card.id == TrackedCard.card_id)
            .where(TrackedCard.active.is_(True))
        )
        rows = result.all()

        if not rows:
            print("No active tracked cards. Add rows to tracked_cards to enable ETL fetching.")
            return

        for tracked, card in rows:
            if not await needs_refresh(db, card.id):
                print(f"[skip] card={card.id} ({card.name}): cached, checked recently")
                continue

            try:
                matched = await fetch_sales_from_providers(card)
            except Exception as e:
                print(f"[error] card={card.id} ({card.name}): {e!r} — skipping, will retry next run")
                continue

            valid = []
            for sale in matched:
                reason = validate_sale(sale)
                if reason:
                    print(f"[skip] card={card.id} sale={sale.source_sale_id}: {reason}")
                else:
                    valid.append(sale)

            await upsert_sales(db, card.id, valid)
            await mark_checked(db, card.id)
            print(f"[ok] card={card.id} ({card.name}): matched={len(matched)} saved={len(valid)}")


if __name__ == "__main__":
    asyncio.run(main())
