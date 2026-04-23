from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import receipts, expenses
from app.core.config import settings
from app.db.database import engine, Base
from app.core import firebase
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

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(receipts.router, prefix=settings.API_V1_STR + "/receipts", tags=["receipts"])
app.include_router(expenses.router, prefix=settings.API_V1_STR + "/expenses", tags=["expenses"])

@app.get("/")
def root():
    return {"message": "Welcome to the Intelligent Receipt System"}
