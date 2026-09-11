import asyncio
from collections.abc import AsyncGenerator

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

check_router = APIRouter()


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
