from fastapi import FastAPI

from app.api.routers.health import health_router
from app.config import get_settings


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(health_router)
    get_settings()
    return app


app = create_app()
