from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CardOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    external_id: str
    name: str
    set_id: str
    set_name: str
    card_number: str
    rarity: str | None
    supertype: str | None
    subtypes: str | None
    image_small: str | None
    image_large: str | None
    language: str
    created_at: datetime
    updated_at: datetime


class CardSearchResult(CardOut):
    match_score: int


class CardWithSalesCount(CardOut):
    sales_count: int
