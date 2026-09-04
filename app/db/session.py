from collections.abc import AsyncGenerator

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import get_settings

settings = get_settings()

database_url = sa.URL.create(
    "postgresql+asyncpg",
    username=settings.db.user,
    password=settings.db.password.get_secret_value(),
    host=settings.db.host,
    port=settings.db.port,
    database=settings.db.db,
)
engine = create_async_engine(url=database_url)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
