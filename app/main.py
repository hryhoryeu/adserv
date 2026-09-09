from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.api.routers.health import health_router
from app.config import get_database_url, get_settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[dict, None]:
    app.state.ready = False
    get_settings()
    engine = create_async_engine(url=get_database_url(), echo_pool="debug")
    session_maker = async_sessionmaker(engine, expire_on_commit=False)
    try:
        app.state.ready = True
        yield {"session_maker": session_maker}
    finally:
        app.state.ready = False
        await engine.dispose()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(health_router)
    return app


app = create_app()
