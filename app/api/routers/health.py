from fastapi import HTTPException, status
from fastapi.routing import APIRouter
from sqlalchemy import text

from app.api.deps import SessionDep

health_router = APIRouter()


@health_router.get("/healthz")
async def healthz():
    return {"status": "ok"}


@health_router.get("/readyz")
async def readyz(session: SessionDep):
    try:
        await session.execute(text("SELECT 1"))
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE) from exc
    return {"status": "ok"}
