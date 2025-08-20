import asyncio
from starlette.types import ASGIApp, Receive, Scope, Send


class RequestTimeoutMiddleware:
    def __init__(self, app: ASGIApp, timeout: int = 15) -> None:
        self.app = app
        self.timeout = timeout

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        async def call_next() -> None:
            await self.app(scope, receive, send)

        try:
            await asyncio.wait_for(call_next(), timeout=self.timeout)
        except asyncio.TimeoutError:
            from starlette.responses import JSONResponse

            response = JSONResponse(
                {"detail": "Request timed out"}, status_code=504
            )
            await response(scope, receive, send)


