import uuid
from contextvars import ContextVar

from starlette.datastructures import MutableHeaders
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from app.core.middleware import headers

request_id_var: ContextVar[str] = ContextVar("request_id", default="-")


class RequestIDMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request_id = str(
            uuid.uuid4()
        )  # we don't check for incoming since it can be compromised
        scope.setdefault("state", {})["request_id"] = request_id
        request_id_var.set(request_id)

        async def send_wrapper(message: Message) -> None:
            if message["type"] == "http.response.start":
                MutableHeaders(scope=message).append(headers.X_REQUEST_ID, request_id)
            await send(message)

        await self.app(scope, receive, send_wrapper)
