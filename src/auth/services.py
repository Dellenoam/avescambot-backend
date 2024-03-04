from datetime import datetime, timedelta
from typing import List, Tuple
import uuid
from fastapi import HTTPException
from .schemas import AccessToken, AuthUser, UserAsResponse, UserCreate, UserLogin
from .utils import encode_jwt, validate_password_hash
from .repository import AuthRepository
from config import settings

repo = AuthRepository()


async def process_user_registration(user: UserCreate) -> UserAsResponse:
    return await repo.create_user(user)


async def validate_auth_user(user: UserLogin) -> AuthUser:
    unauthenticated_exception = HTTPException(
        status_code=401, detail="Could not validate credentials"
    )

    user_from_db = await repo.get_user_by_email(user.email)

    if not user_from_db:
        raise unauthenticated_exception

    if validate_password_hash(user.password, user_from_db.hashed_password) is False:
        raise unauthenticated_exception

    if not user_from_db.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")

    # if not user_from_db.is_verified:
    #     raise HTTPException(status_code=403, detail="User not verified")

    return AuthUser(
        id=user_from_db.id,
        username=user_from_db.username,
        email=user_from_db.email,
        created_at=user_from_db.created_at,
        fingerprint=user.fingerprint,
    )


async def create_access_token_and_refresh_session(
    user: AuthUser,
) -> Tuple[str, AccessToken]:
    access_token = _create_access_token(user.id)
    refresh_session = await _create_refresh_session(user.id, user.fingerprint)

    return refresh_session, AccessToken(access_token=access_token)


async def refresh_access_token_and_refresh_session(
    refresh_session_uuid: str, fingerprint: str
) -> Tuple[str, AccessToken]:
    refresh_session = await repo.get_refresh_session_by_refresh_session_uuid(
        refresh_session_uuid
    )

    if not refresh_session:
        raise HTTPException(status_code=401, detail="Refresh session not found")

    await repo.delete_refresh_session(refresh_session)

    if (
        refresh_session.exp < datetime.utcnow()
        or refresh_session.fingerprint != fingerprint
    ):
        raise HTTPException(status_code=401, detail="Invalid refresh session")

    access_token = _create_access_token(int(refresh_session.sub))
    new_refresh_session = await _create_refresh_session(
        int(refresh_session.sub), refresh_session.fingerprint
    )

    return new_refresh_session, AccessToken(access_token=access_token)


def _create_access_token(user_id: int, scopes: List[str] = []) -> str:
    if not user_id:
        raise ValueError("User ID is required to create access token")

    return encode_jwt(
        payload={
            "sub": user_id,
            "scopes": scopes,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow()
            + timedelta(minutes=settings.token.access_token_expire_minutes),
        }
    )


async def _create_refresh_session(user_id: int, fingerprint: str) -> str:
    if not user_id:
        ValueError("User ID is required to create refresh session")

    if not fingerprint:
        ValueError("Fingerprint is required to create refresh session")

    refresh_session_uuid = str(uuid.uuid4())
    await repo.create_refresh_session(
        sub=user_id,
        fingerprint=fingerprint,
        refresh_session_uuid=refresh_session_uuid,
        iat=datetime.utcnow(),
        exp=datetime.utcnow() + timedelta(days=settings.token.refresh_session_expire_days),
    )

    return refresh_session_uuid
