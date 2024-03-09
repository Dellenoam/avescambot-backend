from typing import Annotated
from fastapi import APIRouter, Cookie, Depends, Response
from auth.dependencies import auth_service, token_service
from .services import AuthService, TokenService
from .schemas import (
    AccessToken,
    UserCreate,
    UserAsResponse,
    UserDetails,
    UserLogin,
)
from config import settings

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
async def register_user(
    user: UserCreate, auth_service: Annotated[AuthService, Depends(auth_service)]
) -> UserAsResponse:
    """
    Route to register a new user.

    Args:
        user (UserCreate): Pydantic model representing the user to register.
        auth_service (Annotated[AuthService, Depends(auth_service)]): The authentication service.

    Returns:
        UserAsResponse: Pydantic model representing the registered user.
    """
    new_user = await auth_service.create_new_user(user)
    return new_user


@router.post("/login")
async def login_user(
    response: Response,
    user: UserLogin,
    auth_service: Annotated[AuthService, Depends(auth_service)],
    token_service: Annotated[TokenService, Depends(token_service)],
) -> AccessToken:
    """
    Route to login a user.

    Parameters:
        response (Response): The response object.
        user (UserLogin): Pydantic model representing the user to login.
        auth_service (AuthService): The authentication service.
        token_service (TokenService): The token service.

    Returns:
        AccessToken: Pydantic model representing the access token.
    """
    auth_user = await auth_service.validate_user(user)
    tokens = await token_service.create_access_token_and_refresh_token(auth_user)

    response.set_cookie(
        key="refresh_token_uuid",
        value=str(tokens.refresh_token_uuid),
        httponly=True,
        max_age=settings.token.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        path=settings.cookie.PATHS,
        secure=settings.cookie.SECURE_FLAG,
    )

    return AccessToken(access_token=tokens.access_token)


@router.post("/refresh")
async def refresh_access_token(
    response: Response,
    refresh_token_uuid: Annotated[str, Cookie()],
    token_service: Annotated[TokenService, Depends(token_service)],
    user_details: UserDetails,
) -> AccessToken:
    """
    Route to refresh the access token.

    Args:
        response (Response): The response object.
        refresh_token_uuid (str): The UUID of the refresh token.
        token_service (TokenService): The token service.
        user_details (UserDetails): Pydantic model representing the user details.

    Returns:
        AccessToken: Pydantic model representing the access token.
    """
    tokens = await token_service.renew_access_token_and_refresh_token(
        refresh_token_uuid, user_details.fingerprint
    )

    response.set_cookie(
        key="refresh_token_uuid",
        value=tokens.refresh_token_uuid,
        httponly=True,
        max_age=settings.token.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        path=settings.cookie.PATHS,
        secure=settings.cookie.SECURE_FLAG,
    )

    return AccessToken(access_token=tokens.access_token)
