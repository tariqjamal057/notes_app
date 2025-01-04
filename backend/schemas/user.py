from datetime import date, timedelta

from pydantic import BaseModel, EmailStr, Field

from backend.constant import ACCESS_EXPIRES, REFRESH_EXPIRES


class RegisterUser(BaseModel):
    username: str
    email: EmailStr
    mobile_number: str
    password: str = Field(exclude=True)


class UserResponse(RegisterUser):
    id: str
    last_update: date
    created_on: date


class UserAuth(BaseModel):
    email: EmailStr
    password: str


class AccessToken(BaseModel):
    access_token: str


class RefreshToken(AccessToken):
    refresh_token: str
