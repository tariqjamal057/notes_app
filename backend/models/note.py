import importlib
from datetime import date, datetime
from uuid import uuid4

from beanie import Document

from backend.models.base import BaseModel

NoteRequestModel = importlib.import_module("backend.schemas").NoteRequest


class Note(NoteRequestModel, BaseModel):
    """Note model class."""

    pass

    class Settings:
        name = "notes"  # MongoDB collection name
