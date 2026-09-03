from fastapi import FastAPI

from app.api.routers.health import health_router


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(health_router)
    return app


app = create_app()
