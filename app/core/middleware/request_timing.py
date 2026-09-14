from time import time

from starlette.datastructures import MutableHeaders
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from app.core.middleware import headers


class TimingMiddleware(ASGIApp):
    def __init__(self, app: ASGIApp):
        self.app = app
        self.start_time = time()

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        request_timing = str(time() - self.start_time)
        scope.setdefault("state", {})["request_timing"] = request_timing

        async def send_wrapper(message: Message) -> None:
            if message["type"] == "http.response.start":
                MutableHeaders(scope=message).append(
                    headers.X_PROCESS_TIME, request_timing
                )
            await send(message)

        await self.app(scope, receive, send_wrapper)
