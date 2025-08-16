import fastapi
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(fastapi.exceptions.ResponseValidationError)
    async def not_found_exception_handler(request: Request, exc: fastapi.exceptions.ResponseValidationError):
        return ORJSONResponse(status_code=404, content="Item not found!")

    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)