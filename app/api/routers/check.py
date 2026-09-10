import asyncio
from collections.abc import AsyncGenerator

from fastapi import APIRouter, Request, Response
from fastapi.responses import StreamingResponse
from starlette.background import BackgroundTask

check_router = APIRouter()


async def _ticker() -> AsyncGenerator[bytes, None]:
    for i in range(5):
        yield f"chunk {i}\n".encode()
        await asyncio.sleep(1)


@check_router.get("/whoami")
async def whoami(request: Request) -> Response:
    return {"header": request.state.request_id}


@check_router.get("/stream")
async def stream(request: Request) -> StreamingResponse:
    return StreamingResponse(_ticker(), media_type="text/plain")


@check_router.get("/zero")
async def zero():
    return 1 / 0


@check_router.get("/bg")
async def bg(request: Request) -> Response:
    async def after() -> None:
        print("BG start")
        await asyncio.sleep(2)
        print("BG finish")

    return Response(content="done\n", background=BackgroundTask(after))
