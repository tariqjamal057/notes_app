from contextlib import asynccontextmanager

from beanie import init_beanie
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from backend.models import Note, User
from backend.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize application services."""
    client = AsyncIOMotorClient(settings.MONGO_URI)
    app.db = client.notes_app
    await init_beanie(database=app.db, document_models=[User, Note])
    yield
    client.close()
