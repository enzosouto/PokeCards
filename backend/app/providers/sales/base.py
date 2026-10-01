from abc import ABC, abstractmethod
from datetime import datetime

from pydantic import BaseModel


class NormalizedSale(BaseModel):
    source: str
    provider: str
    source_sale_id: str
    title: str
    price: float
    currency: str
    shipping: float | None = None
    condition: str | None = None
    grading_company: str | None = None
    grade: str | None = None
    listing_type: str | None = None
    sold_at: datetime
    listing_url: str | None = None


class BaseSalesProvider(ABC):
    @abstractmethod
    async def search_sales(self, query: str) -> list[NormalizedSale]: ...
