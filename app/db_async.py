from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)

from .config import ASYNC_DB_URL
from .models import Base

# Async engine pro PostgreSQL přes asyncpg
async_engine = create_async_engine(
    ASYNC_DB_URL,
    echo=False,
    future=True,
)

# Továrna na async session
AsyncSessionLocal = async_sessionmaker(
    async_engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def init_db_async() -> None:
    """
    Vytvoří tabulky v databázi pomocí async engine.
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)