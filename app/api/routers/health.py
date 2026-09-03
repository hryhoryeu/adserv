from fastapi.routing import APIRouter

from app.config import get_db_settings

settings = get_db_settings()
health_router = APIRouter()


@health_router.get("/healthz")
async def healthz():
    return {"msg": f"healthz. {settings.database_url}"}


@health_router.get("/readyz")
async def readyz():
    return {"msg": "readyz"}
