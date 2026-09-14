from logging import getLogger
from time import perf_counter

from starlette.datastructures import MutableHeaders
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from app.core import headers

logger = getLogger(__name__)


class TimingMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        start_time = perf_counter()
        status_code = 500

        async def send_wrapper(message: Message) -> None:
            nonlocal status_code
            if message["type"] == "http.response.start":
                status_code = message["status"]
                ellapsed_time_ms = (perf_counter() - start_time) * 1000
                ellapsed_time_ms_formatted = f"{ellapsed_time_ms:.2f}"

                MutableHeaders(scope=message).append(
                    headers.X_PROCESS_TIME, ellapsed_time_ms_formatted
                )
            await send(message)

        await self.app(scope, receive, send_wrapper)

        logger.info(
            "request",
            extra={
                "method": scope["method"],
                "path": scope["path"],
                "status": status_code,
                "duration_ms": round((perf_counter() - start_time) * 1000, 2),
            },
        )
