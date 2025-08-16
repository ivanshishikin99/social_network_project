from fastapi import FastAPI
from slowapi.middleware import SlowAPIMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

from middleware.logging_middleware import logging_middleware


def register_middleware(app: FastAPI):
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_headers=["*"], allow_methods=["*"])

    app.add_middleware(BaseHTTPMiddleware, dispatch=logging_middleware)

    app.add_middleware(SlowAPIMiddleware)

