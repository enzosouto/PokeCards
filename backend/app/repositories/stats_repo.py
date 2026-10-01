from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sale import Sale


class CardStats:
    def __init__(self, latest_sale, latest_sale_date, average, median, minimum, maximum, count):
        self.latest_sale = latest_sale
        self.latest_sale_date = latest_sale_date
        self.average = average
        self.median = median
        self.minimum = minimum
        self.maximum = maximum
        self.count = count


async def compute_stats(db: AsyncSession, card_id: int, days: int | None = None) -> CardStats:
    query = select(Sale).where(Sale.card_id == card_id)
    if days is not None:
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        query = query.where(Sale.sold_at >= cutoff)

    latest_row = (await db.execute(query.order_by(Sale.sold_at.desc()).limit(1))).scalar_one_or_none()

    subq = query.subquery()
    agg_query = select(
        func.avg(subq.c.price),
        func.percentile_cont(0.5).within_group(subq.c.price),
        func.min(subq.c.price),
        func.max(subq.c.price),
        func.count(subq.c.id),
    )
    average, median, minimum, maximum, count = (await db.execute(agg_query)).one()

    return CardStats(
        latest_sale=float(latest_row.price) if latest_row else None,
        latest_sale_date=latest_row.sold_at if latest_row else None,
        average=float(average) if average is not None else None,
        median=float(median) if median is not None else None,
        minimum=float(minimum) if minimum is not None else None,
        maximum=float(maximum) if maximum is not None else None,
        count=count or 0,
    )
