from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SaleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    provider: str
    title: str
    price: float
    currency: str
    original_price: float | None
    original_currency: str | None
    shipping: float | None
    condition: str | None
    grading_company: str | None
    grade: str | None
    listing_type: str | None
    sold_at: datetime
    listing_url: str | None


class RecentSaleOut(SaleOut):
    card_id: int
    card_name: str
    card_number: str
    set_name: str
    image_small: str | None
