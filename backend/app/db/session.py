from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.config import settings

engine = create_async_engine(
    settings.database_url,
    echo=False,
    # Neon's pooled connections can be handed back with a stale/empty search_path
    # from an unrelated session — set it explicitly on every new connection instead
    # of trusting whatever the pooler reused.
    connect_args={"server_settings": {"search_path": "public"}},
)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_db():
    async with SessionLocal() as session:
        yield session
