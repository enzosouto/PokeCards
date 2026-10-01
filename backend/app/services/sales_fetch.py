from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.matching.card_matcher import filter_matching_sales
from app.models.card import Card
from app.providers.sales.base import NormalizedSale
from app.repositories.sale_repo import upsert_sales
from app.repositories.tracked_card_repo import mark_checked


async def fetch_sales_from_providers(card: Card) -> list[NormalizedSale]:
    """Query name + number only — full set names rarely appear verbatim in eBay titles
    and were killing recall entirely. Relevance is enforced by filter_matching_sales."""
    query = f"{card.name} {card.card_number}"
    sales: list[NormalizedSale] = []

    if settings.the_card_api_key:
        from app.providers.sales.the_card_api import TheCardApiProvider

        sales = await TheCardApiProvider().search_sales(query)

    if not sales and settings.trawl_api_key:
        from app.providers.sales.trawl import TrawlProvider

        sales = await TrawlProvider().search_sales(query)

    return filter_matching_sales(card, sales)


async def refresh_card_sales(db: AsyncSession, card: Card) -> list[NormalizedSale]:
    sales = await fetch_sales_from_providers(card)
    await upsert_sales(db, card.id, sales)
    await mark_checked(db, card.id)
    return sales
