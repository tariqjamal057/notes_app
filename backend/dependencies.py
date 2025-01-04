from fastapi import Security, status
from fastapi.responses import JSONResponse
from fastapi_jwt import JwtAuthorizationCredentials

from backend.models.user import User, access_security


async def get_auth_user(
    auth: JwtAuthorizationCredentials = Security(access_security),
) -> User:
    """Retrieves the authenticated user from the JWT authorization credentials.

    If no authorization credentials are found, returns a 401 Unauthorized response. If the token is
    invalid or the user ID is missing, returns a 401 Unauthorized response. If the user is not
    found, returns a 401 Unauthorized response. If an unexpected error occurs, returns a 500
    Internal Server Error response.
    """
    try:
        if not auth:
            return JSONResponse(
                content={"message": "No authorization credentials found."},
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        user_id = auth.subject.get("id", None)
        if not user_id:
            return JSONResponse(
                content={"message": "Invalid token passed."},
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        user = await User.get_by_id(user_id)
        if not user:
            return JSONResponse(
                content={"message": "Invalid token data."},
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        return user
    except Exception:
        return JSONResponse(
            content={"message": "Unexpected error occured."},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
