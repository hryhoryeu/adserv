from typing import Annotated

from fastapi import Depends
from fastapi.routing import APIRouter

from app.config import PostgresSettings, get_db_settings

health_router = APIRouter()


@health_router.get("/healthz")
async def healthz():
    return {"msg": "healthz"}


@health_router.get("/readyz")
async def readyz(settings: Annotated[PostgresSettings, Depends(get_db_settings)]):
    return {"msg": "readyz"}
