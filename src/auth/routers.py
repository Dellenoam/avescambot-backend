from typing import Annotated
from fastapi import APIRouter, Body, Cookie, Depends, Response
from .services import (
    create_access_token_and_refresh_session,
    process_user_registration,
    refresh_access_token_and_refresh_session,
    validate_auth_user,
)
from .schemas import AccessToken, AuthUser, UserCreate, UserAsResponse
from src.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
async def register_user(user: UserCreate) -> UserAsResponse:
    return await process_user_registration(user)


@router.post("/login")
async def login_user(
    response: Response,
    user: AuthUser = Depends(validate_auth_user),
) -> AccessToken:
    refresh_session_uuid, access_token = await create_access_token_and_refresh_session(
        user
    )

    response.set_cookie(
        key="refresh_session_uuid",
        value=str(refresh_session_uuid),
        httponly=True,
        max_age=settings.refresh_session_expire_days * 24 * 60 * 60,
        path="/auth/refresh",
    )

    return access_token


@router.post("/refresh")
async def refresh_access_token(
    response: Response, fingerprint: Annotated[str, Body(embed=True)], refresh_session_uuid: Annotated[str, Cookie()]
) -> AccessToken:
    refresh_session_uuid, access_token = await refresh_access_token_and_refresh_session(
        refresh_session_uuid, fingerprint
    )

    response.set_cookie(
        key="refresh_session_uuid",
        value=str(refresh_session_uuid),
        httponly=True,
        max_age=settings.refresh_session_expire_days * 24 * 60 * 60,
        path="/auth/refresh",
    )

    return access_token
