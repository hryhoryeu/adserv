from typing import Annotated

from fastapi import Depends
from fastapi.routing import APIRouter

from app.config import get_db_settings

health_router = APIRouter()


@health_router.get("/healthz")
async def healthz(settings: Annotated[dict, Depends(get_db_settings)]):
    return {"msg": f"healthz. {settings.database_url}"}


@health_router.get("/readyz")
async def readyz():
    return {"msg": "readyz"}
