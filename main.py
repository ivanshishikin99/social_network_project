from contextlib import asynccontextmanager

from fastapi import FastAPI

import uvicorn

from utils.db_helper import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db_helper.engine.dispose()

app = FastAPI(lifespan=lifespan)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)