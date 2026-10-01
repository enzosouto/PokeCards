import asyncio
import re

import httpx

from app.core.config import settings
from app.providers.cards.base import CardProvider, NormalizedCard

BASE_URL = "https://api.pokemontcg.io/v2"


async def _get_with_retry(client: httpx.AsyncClient, url: str, **kwargs) -> httpx.Response:
    """pokemontcg.io's public tier returns occasional 500/502s; retry with backoff."""
    last_error: Exception | None = None
    for attempt in range(5):
        try:
            resp = await client.get(url, **kwargs)
        except httpx.TransportError as e:
            last_error = e
            await asyncio.sleep(0.5 * (attempt + 1))
            continue
        if resp.status_code < 500:
            return resp
        last_error = httpx.HTTPStatusError(
            f"Server error '{resp.status_code}'", request=resp.request, response=resp
        )
        await asyncio.sleep(0.5 * (attempt + 1))
    raise last_error


def _build_query(query: str) -> str:
    """Turn free text like 'Charizard ex 199/165' into a pokemontcg.io lucene query."""
    query = query.strip()
    number_match = re.search(r"(\d+)\s*/\s*\d+", query)
    parts = []
    name = query
    if number_match:
        name = query[: number_match.start()].strip()
        parts.append(f'number:{number_match.group(1)}')
    if name:
        parts.append(f'name:"{name}*"')
    return " ".join(parts) if parts else f'name:"{query}*"'


def _to_normalized(card: dict) -> NormalizedCard:
    images = card.get("images", {})
    set_info = card.get("set", {})
    return NormalizedCard(
        external_id=card["id"],
        name=card["name"],
        set_id=set_info.get("id", ""),
        set_name=set_info.get("name", ""),
        card_number=card.get("number", ""),
        rarity=card.get("rarity"),
        supertype=card.get("supertype"),
        subtypes=card.get("subtypes", []),
        image_small=images.get("small"),
        image_large=images.get("large"),
    )


class PokemonTcgIoProvider(CardProvider):
    def __init__(self):
        self._headers = {"X-Api-Key": settings.pokemontcg_api_key} if settings.pokemontcg_api_key else {}

    async def search(self, query: str) -> list[NormalizedCard]:
        params = {"q": _build_query(query), "pageSize": 25}
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await _get_with_retry(client, f"{BASE_URL}/cards", params=params, headers=self._headers)
            resp.raise_for_status()
            data = resp.json()
        return [_to_normalized(c) for c in data.get("data", [])]

    async def get_by_id(self, external_id: str) -> NormalizedCard | None:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await _get_with_retry(client, f"{BASE_URL}/cards/{external_id}", headers=self._headers)
            if resp.status_code == 404:
                return None
            resp.raise_for_status()
            data = resp.json()
        return _to_normalized(data["data"])
