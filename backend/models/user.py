from datetime import date, datetime, timedelta
from uuid import uuid4

from beanie import Document
from fastapi_jwt import JwtAccessBearer, JwtRefreshBearer
from passlib.context import CryptContext
from pydantic import EmailStr

from backend.constant import ACCESS_EXPIRES, REFRESH_EXPIRES
from backend.models.base import BaseModel
from backend.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
import importlib

UserRequestModel = importlib.import_module("backend.schemas").RegisterUser

access_security = JwtAccessBearer(
    settings.SECRET_KEY,
    access_expires_delta=ACCESS_EXPIRES,
    refresh_expires_delta=REFRESH_EXPIRES,
)

refresh_security = JwtRefreshBearer(
    settings.SECRET_KEY,
    access_expires_delta=ACCESS_EXPIRES,
    refresh_expires_delta=REFRESH_EXPIRES,
)


class User(UserRequestModel, BaseModel):
    """User model class."""

    pass

    class Settings:
        name = "users"  # MongoDB collection name

    @classmethod
    def get_password(cls, plain_password: str):
        """Hash the provided plain password."""
        return pwd_context.hash(plain_password)

    async def verify_password(self, plain_password: str):
        """Verify if the provided plain password matches the hashed password."""
        return pwd_context.verify(plain_password, self.password)
