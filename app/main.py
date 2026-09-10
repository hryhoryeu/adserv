from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.api.routers.check import check_router
from app.api.routers.health import health_router
from app.config import get_database_url, get_settings
from app.core.middleware.request_id import RequestIDMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[dict, None]:
    app.state.ready = False
    get_settings()
    engine = create_async_engine(url=get_database_url(), pool_size=5, max_overflow=10)
    session_maker = async_sessionmaker(engine, expire_on_commit=False)
    try:
        app.state.ready = True
        yield {"session_maker": session_maker}
    finally:
        app.state.ready = False
        await engine.dispose()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.add_middleware(RequestIDMiddleware)
    app.include_router(health_router)
    app.include_router(check_router)
    return app


app = create_app()
