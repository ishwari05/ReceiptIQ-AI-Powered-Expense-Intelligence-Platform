from fastapi import FastAPI
from app.api.routes import receipts
from app.core.config import settings
from app.db.database import engine, Base
import logging
from contextlib import asynccontextmanager

logging.basicConfig(level=logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup (for testing purposes)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

app.include_router(receipts.router, prefix=settings.API_V1_STR, tags=["receipts"])

@app.get("/")
def root():
    return {"message": "Welcome to the Intelligent Receipt System"}
