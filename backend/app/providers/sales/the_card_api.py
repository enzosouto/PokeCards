import httpx

from app.core.config import settings
from app.providers.sales.base import BaseSalesProvider, NormalizedSale

BASE_URL = "https://www.thecardapi.com/api/v1/market"


def _to_normalized(sale: dict) -> NormalizedSale:
    return NormalizedSale(
        source=sale.get("platform", "ebay").lower(),
        provider="the_card_api",
        source_sale_id=str(sale["id"]),
        title=sale["title"],
        price=sale["price"],
        currency=sale.get("currency", "USD"),
        shipping=sale.get("shipping_price"),
        condition=sale.get("condition"),
        grading_company=sale.get("grader"),
        grade=sale.get("grade"),
        listing_type=sale.get("listing_type"),
        sold_at=sale["sold_at"],
        listing_url=sale.get("listing_url"),
    )


class TheCardApiProvider(BaseSalesProvider):
    """Requires THE_CARD_API_KEY (sign up at https://www.thecardapi.com). Free tier: 5,000 rows/day, 3-day lookback."""

    def __init__(self):
        if not settings.the_card_api_key:
            raise RuntimeError("THE_CARD_API_KEY not configured")
        self._headers = {"x-market-api-key": settings.the_card_api_key}

    async def search_sales(self, query: str) -> list[NormalizedSale]:
        params = {
            "q": query,
            "platform": "ebay",
            "sort": "date_desc",
            "limit": 50,
        }
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(f"{BASE_URL}/sales", params=params, headers=self._headers)
            resp.raise_for_status()
            data = resp.json()
        return [_to_normalized(s) for s in data.get("data", [])]
