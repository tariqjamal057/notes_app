from fastapi import APIRouter, Security, status
from fastapi.responses import JSONResponse
from fastapi_jwt import JwtAuthorizationCredentials

from backend.models import User
from backend.models.user import access_security, refresh_security
from backend.schemas.user import AccessToken, RefreshToken, RegisterUser, UserAuth

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.post("/register")
async def register(user_request: RegisterUser):
    """Endpoint to register the user."""
    try:
        user: User = await User.find_one({"email": user_request.email})
        if user:
            return JSONResponse(
                content={"message": "User already exists"},
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        await User.add(
            user_request.model_dump() | {"password": User.get_password(user_request.password)}
        )
        return JSONResponse(
            content={"message": "User registered successfully"},
            status_code=status.HTTP_201_CREATED,
        )
    except Exception:
        return JSONResponse(
            content={"message": "Unexpected error occurred while registering the user"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
