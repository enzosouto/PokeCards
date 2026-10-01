import time

import httpx

RATES_URL = "https://api.frankfurter.dev/v1/latest"
CACHE_TTL_SECONDS = 24 * 3600

_rates: dict[str, float] = {}
_fetched_at: float = 0.0


async def _get_rates() -> dict[str, float]:
    global _fetched_at
    if _rates and time.time() - _fetched_at < CACHE_TTL_SECONDS:
        return _rates

    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(RATES_URL, params={"base": "USD"})
        resp.raise_for_status()
        data = resp.json()

    _rates.clear()
    _rates.update(data["rates"])
    _fetched_at = time.time()
    return _rates


async def to_usd(amount: float, currency: str) -> float:
    """1 USD = rates[currency] units of that currency."""
    currency = currency.upper()
    if currency == "USD":
        return amount
    rates = await _get_rates()
    rate = rates.get(currency)
    if rate is None:
        return amount  # unknown currency: leave unconverted rather than guess
    return round(amount / rate, 2)
