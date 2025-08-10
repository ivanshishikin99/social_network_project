import asyncio
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from fastapi import FastAPI

import uvicorn
from fastapi.responses import ORJSONResponse
from prometheus_fastapi_instrumentator import Instrumentator

from core.config import settings
from middleware.register_middleware import register_middleware
from utils.db_helper import db_helper

from api_v1 import router as api_v1_router
from utils.delete_verification_token import clean_verification_token_table


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(
        f"redis://{settings.redis_config.hostname}:{settings.redis_config.port}"
    )
    FastAPICache.init(RedisBackend(redis), prefix=settings.redis_config.prefix)
    asyncio.create_task(clean_verification_token_table())
    yield
    await db_helper.engine.dispose()

app = FastAPI(lifespan=lifespan, title="Social Network", default_response_class=ORJSONResponse)

instrumentator = Instrumentator(should_group_status_codes=False,
                                excluded_handlers=["/metrics"])

instrumentator.instrument(app).expose(app)

register_middleware(app=app)

app.include_router(api_v1_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)