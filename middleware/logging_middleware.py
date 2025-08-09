from typing import Callable, Awaitable

from starlette.requests import Request
from starlette.responses import Response

from logger import log


class Logging_Middleware:
    async def __call__(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        result = await call_next(request)
        log.info("Request method %s to %s", request.method, request.url)
        return result

logging_middleware = Logging_Middleware()
