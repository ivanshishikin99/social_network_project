from contextlib import asynccontextmanager

from fastapi import FastAPI

import uvicorn

from utils.db_helper import db_helper

from api_v1 import router as api_v1_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db_helper.engine.dispose()

app = FastAPI(lifespan=lifespan)

app.include_router(api_v1_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)