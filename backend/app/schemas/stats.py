from datetime import datetime

from pydantic import BaseModel


class CardStatsOut(BaseModel):
    latest_sale: float | None
    latest_sale_date: datetime | None
    average: float | None
    median: float | None
    minimum: float | None
    maximum: float | None
    count: int
