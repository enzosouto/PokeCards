from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.session import get_db
from app.repositories.card_repo import get_card
from app.repositories.sale_repo import list_recent_sales, list_sales
from app.repositories.stats_repo import compute_stats
from app.repositories.tracked_card_repo import needs_refresh
from app.schemas.sale import RecentSaleOut, SaleOut
from app.schemas.stats import CardStatsOut
from app.services.sales_fetch import refresh_card_sales

router = APIRouter(prefix="/api/cards", tags=["sales"])
recent_sales_router = APIRouter(prefix="/api/sales", tags=["sales"])


@recent_sales_router.get("/recent", response_model=list[RecentSaleOut])
async def get_recent_sales(limit: int = 50, db: AsyncSession = Depends(get_db)):
    rows = await list_recent_sales(db, limit)
    return [
        RecentSaleOut(
            **SaleOut.model_validate(sale).model_dump(),
            card_id=card.id,
            card_name=card.name,
            card_number=card.card_number,
            set_name=card.set_name,
            image_small=card.image_small,
        )
        for sale, card in rows
    ]


@router.get("/{card_id}/sales", response_model=list[SaleOut])
async def get_sales(card_id: int, db: AsyncSession = Depends(get_db)):
    card = await get_card(db, card_id)
    if card is None:
        raise HTTPException(404, "card not found")

    if (settings.the_card_api_key or settings.trawl_api_key) and await needs_refresh(db, card_id):
        try:
            await refresh_card_sales(db, card)
        except Exception:
            pass  # provider unavailable (e.g. quota exceeded) — serve whatever is cached

    return await list_sales(db, card_id)


@router.get("/{card_id}/stats", response_model=CardStatsOut)
async def get_stats(card_id: int, days: int | None = None, db: AsyncSession = Depends(get_db)):
    card = await get_card(db, card_id)
    if card is None:
        raise HTTPException(404, "card not found")
    stats = await compute_stats(db, card_id, days)
    return CardStatsOut(
        latest_sale=stats.latest_sale,
        latest_sale_date=stats.latest_sale_date,
        average=stats.average,
        median=stats.median,
        minimum=stats.minimum,
        maximum=stats.maximum,
        count=stats.count,
    )
