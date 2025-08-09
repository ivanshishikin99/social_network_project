import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

import uvicorn

from middleware.register_middleware import register_middleware
from utils.db_helper import db_helper

from api_v1 import router as api_v1_router
from utils.delete_verification_token import clean_verification_token_table


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(clean_verification_token_table())
    yield
    await db_helper.engine.dispose()

app = FastAPI(lifespan=lifespan)

register_middleware(app=app)

app.include_router(api_v1_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)