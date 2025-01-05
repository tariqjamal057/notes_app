from fastapi import APIRouter, Security, status
from fastapi.responses import JSONResponse
from fastapi_jwt import JwtAuthorizationCredentials

from backend.models.user import User, access_security, refresh_security
from backend.schemas.user import AccessToken, RefreshToken, UserAuth

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/login", response_model=RefreshToken)
async def login(user_request: UserAuth) -> RefreshToken:
    """Endpoint to authenticate user and get access and refresh tokens."""
    try:
        user: User = await User.find_one({"email": user_request.email})
        if not user:
            return JSONResponse(
                content={"message": "User not found"},
                status_code=status.HTTP_404_NOT_FOUND,
            )
        if not await user.verify_password(user_request.password):
            return JSONResponse(
                content={"message": "Invalid Password"},
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        access_token = access_security.create_access_token(user.jwt_subject)
        refresh_token = refresh_security.create_refresh_token(user.jwt_subject)
        return {"access_token": access_token, "refresh_token": refresh_token}
    except Exception:
        return JSONResponse(
            content={"message": "Unexpected error occurred while registering the user"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@auth_router.post("/refresh", response_model=AccessToken)
async def refresh(
    auth: JwtAuthorizationCredentials = Security(refresh_security),
) -> AccessToken:
    """Endpoint to refresh access token."""
    access_token = access_security.create_refresh_token(subject=auth.subject)
    return {"access_token": access_token}
