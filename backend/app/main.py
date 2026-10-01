from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.cards import router as cards_router
from app.api.routes.sales import recent_sales_router, router as sales_router
from app.core.config import settings

app = FastAPI(title="PokeMarket API")
app.include_router(cards_router)
app.include_router(sales_router)
app.include_router(recent_sales_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    return {"status": "ok"}
