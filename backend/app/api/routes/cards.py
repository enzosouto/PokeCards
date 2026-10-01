from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.matching.card_matcher import parse_query, score
from app.providers.cards.pokemontcg import PokemonTcgIoProvider
from app.repositories.card_repo import get_all_cards, get_card, get_top_cards, upsert_card
from app.schemas.card import CardOut, CardSearchResult, CardWithSalesCount

router = APIRouter(prefix="/api/cards", tags=["cards"])
_provider = PokemonTcgIoProvider()

MIN_MATCH_SCORE = 25


@router.get("/search", response_model=list[CardSearchResult])
async def search_cards(q: str, db: AsyncSession = Depends(get_db)):
    if not q or len(q.strip()) < 2:
        raise HTTPException(400, "query too short")

    parsed = parse_query(q)
    results = await _provider.search(q)

    scored = [(c, score(c, parsed)) for c in results]
    scored = [(c, s) for c, s in scored if s >= MIN_MATCH_SCORE] or list(scored)
    scored.sort(key=lambda pair: pair[1], reverse=True)

    out = []
    for normalized, s in scored[:20]:
        card = await upsert_card(db, normalized)
        await db.commit()
        out.append(CardSearchResult(match_score=s, **CardOut.model_validate(card).model_dump()))
    return out


@router.get("", response_model=list[CardWithSalesCount])
async def list_cards(limit: int = 200, offset: int = 0, db: AsyncSession = Depends(get_db)):
    rows = await get_all_cards(db, limit, offset)
    return [
        CardWithSalesCount(sales_count=count, **CardOut.model_validate(card).model_dump())
        for card, count in rows
    ]


@router.get("/top", response_model=list[CardWithSalesCount])
async def top_cards(limit: int = 12, db: AsyncSession = Depends(get_db)):
    rows = await get_top_cards(db, limit)
    return [
        CardWithSalesCount(sales_count=count, **CardOut.model_validate(card).model_dump())
        for card, count in rows
    ]


@router.get("/{card_id}", response_model=CardOut)
async def get_card_detail(card_id: int, db: AsyncSession = Depends(get_db)):
    card = await get_card(db, card_id)
    if card is None:
        raise HTTPException(404, "card not found")
    return card
