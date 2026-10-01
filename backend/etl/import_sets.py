"""Bulk-import every card from a curated list of popular/valuable sets into the catalog,
then mark them as tracked so etl.fetch_sales picks up real sales for all of them.

Run with: python -m etl.import_sets
"""

import asyncio
import sys

import httpx
from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.tracked_card import TrackedCard
from app.providers.cards.pokemontcg import BASE_URL, _to_normalized
from app.repositories.card_repo import upsert_card

# Popular/high-market-interest sets (real ids confirmed against pokemontcg.io /v2/sets)
SET_IDS = [
    "sv3pt5",  # 151
    "base1",  # Base Set (1999 classic)
]


async def fetch_set_cards(set_id: str) -> list[dict]:
    async with httpx.AsyncClient(timeout=20) as client:
        resp = await client.get(f"{BASE_URL}/cards", params={"q": f"set.id:{set_id}", "pageSize": 250})
        resp.raise_for_status()
        return resp.json()["data"]


async def main():
    sys.stdout.reconfigure(errors="replace")
    async with SessionLocal() as db:
        for set_id in SET_IDS:
            raw_cards = await fetch_set_cards(set_id)
            print(f"[set] {set_id}: {len(raw_cards)} cards")

            for raw in raw_cards:
                normalized = _to_normalized(raw)
                card = await upsert_card(db, normalized)
                await db.commit()

                existing = await db.execute(select(TrackedCard).where(TrackedCard.card_id == card.id))
                if existing.scalar_one_or_none() is None:
                    db.add(TrackedCard(card_id=card.id, active=True))
                    await db.commit()

        print("Done. Run `python -m etl.fetch_sales` to fetch real sales for the new cards.")


if __name__ == "__main__":
    asyncio.run(main())
