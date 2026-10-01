import httpx

from app.core.config import settings
from app.providers.sales.base import BaseSalesProvider, NormalizedSale

BASE_URL = "https://api.trawl.dev/ebay/v1"


def _to_normalized(item: dict) -> NormalizedSale:
    return NormalizedSale(
        source="ebay",
        provider="trawl",
        source_sale_id=str(item["item_id"]),
        title=item["title"],
        price=item["sale_price"],
        currency=item.get("currency", "USD"),
        shipping=item.get("shipping_price"),
        condition=item.get("condition"),
        grading_company=None,
        grade=None,
        listing_type=item.get("buying_format"),
        sold_at=item["date_sold"],
        listing_url=item.get("item_link"),
    )


class TrawlProvider(BaseSalesProvider):
    """Fallback sales provider. Requires TRAWL_API_KEY (sign up at https://trawl.dev). General eBay sold-listings API, not Pokemon-specific — used when TheCardApiProvider is unavailable or returns too few results."""

    def __init__(self):
        if not settings.trawl_api_key:
            raise RuntimeError("TRAWL_API_KEY not configured")
        self._headers = {"x-api-key": settings.trawl_api_key}

    async def search_sales(self, query: str) -> list[NormalizedSale]:
        params = {"query": query, "site": "EBAY_US", "category": "Collectibles"}
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(f"{BASE_URL}/sold", params=params, headers=self._headers)
            resp.raise_for_status()
            data = resp.json()
        return [_to_normalized(i) for i in data.get("results", [])]
