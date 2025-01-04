"""Base model module providing common functionality for all database models.

This module implements shared attributes and methods used across different models including ID
generation, timestamp handling and database operations.
"""

from datetime import date, datetime
from typing import Any
from uuid import uuid4

from beanie import Document
from pytz import timezone


class BaseModel(Document):
    """Base model for all database models."""

    id: str = str(uuid4())
    last_update: date = datetime.now(timezone("Asia/Kolkata")).date()
    created_on: date = datetime.now(timezone("Asia/Kolkata")).date()

    class Settings:
        abstract = True

    @property
    def jwt_subject(self) -> dict[str, Any]:
        """JWT subject for the model instance.

        Returns:
            dict[str, Any]: JWT subject containing the model's ID.
        """
        return {"id": self.id}

    @classmethod
    async def get_by_id(cls, id: str) -> "BaseModel":
        """Retrieve a document by its unique identifier.

        Args:
            id (str): Unique identifier of the document

        Returns:
            BaseModel: Document instance if found, None otherwise
        """
        return await cls.find_one(cls.id == id)

    @classmethod
    async def update_data(cls, instance: "BaseModel", data: dict) -> "BaseModel":
        """Update document instance with provided data.

        Args:
            instance (BaseModel): Document instance to update
            data (dict): Dictionary containing field updates

        Returns:
            BaseModel: Updated document instance
        """
        for key, value in data.items():
            setattr(instance, key, value)
        instance.last_update = datetime.now(timezone("Asia/Kolkata")).date()
        await instance.save()
        return instance

    @classmethod
    async def add(cls, data: dict) -> "BaseModel":
        """Create and save a new document instance.

        Args:
            data (dict): Document field values

        Returns:
            BaseModel: Created document instance
        """
        instance = cls(**data | {"id": str(uuid4())})
        await instance.create()
        return instance
