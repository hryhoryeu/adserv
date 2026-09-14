import asyncio
from collections.abc import AsyncGenerator
from logging import getLogger

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from app.core.middleware.request_id import request_id_var

check_router = APIRouter()
logger = getLogger(__name__)


async def _ticker() -> AsyncGenerator[bytes, None]:
    for i in range(5):
        yield f"chunk {i}\n".encode()
        await asyncio.sleep(1)


@check_router.get("/whoami")
async def whoami(request: Request) -> dict:
    return {"header": request.state.request_id}


@check_router.get("/stream")
async def stream() -> StreamingResponse:
    return StreamingResponse(_ticker(), media_type="text/plain")


@check_router.get("/zero")
async def zero():
    return 0 / 0


_background_tasks: set[asyncio.Task] = set()


@check_router.get("/ctx-gather")
async def ctx_gather() -> dict:
    await asyncio.gather(log_ctx("a"), log_ctx("b"), log_ctx("c"))
    return {"ok": True}


@check_router.get("/ctx-fire")
async def ctx_fire() -> dict:
    task = asyncio.create_task(slow_log())
    _background_tasks.add(task)
    task.add_done_callback(_background_tasks.discard)
    return {"ok": True}


async def log_ctx(tag: str) -> None:
    logger.info("ctx check", extra={"tag": tag, "rid": request_id_var.get()})


async def slow_log() -> None:
    await asyncio.sleep(2)
    logger.info("fire done", extra={"rid": request_id_var.get()})
