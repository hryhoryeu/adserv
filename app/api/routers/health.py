from logging import getLogger

from fastapi import APIRouter, HTTPException, Request, status
from sqlalchemy import text

from app.api.deps import SessionDep

health_router = APIRouter()
logger = getLogger(__name__)


@health_router.get("/healthz")
async def healthz() -> dict:
    logger.info({"all cool"})
    return {"status": "ok"}


@health_router.get("/readyz")
async def readyz(request: Request, session: SessionDep) -> dict:
    if not request.app.state.ready:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
    try:
        await session.execute(text("SELECT 1"))
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE) from exc
    return {"status": "ok"}
