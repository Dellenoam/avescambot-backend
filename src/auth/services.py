from datetime import datetime, timedelta, timezone
from typing import Type
import uuid
from fastapi import HTTPException
from auth.exceptions import UserExistsError
from auth.models import RefreshToken, User
from repository import AbstractRepository
from .schemas import (
    AuthUser,
    Tokens,
    UserAsResponse,
    UserCreate,
    UserLogin,
)
from .utils import encode_jwt, hash_password, validate_password_hash
from config import settings


class AuthService:
    def __init__(self, repo: Type[AbstractRepository[User]]):
        self.repo = repo()

    async def create_new_user(self, user_to_create: UserCreate) -> UserAsResponse:
        """
        Create a new user. Used via CLI

        Args:
            user_to_create (UserCreate): Pydantic model representing the user to create.

        Returns:
            UserAsResponse: Pydantic model representing the created user.
        """
        if await self.repo.get_one(username=user_to_create.username):
            raise UserExistsError("User with this username already exists")
        if await self.repo.get_one(email=user_to_create.email):
            raise UserExistsError("User with this email already exists")

        user_to_create_dict = user_to_create.model_dump()
        user_to_create_dict["hashed_password"] = hash_password(
            user_to_create_dict["password"]
        )
        del user_to_create_dict["password"]

        new_user = await self.repo.add_one(user_to_create_dict)
        new_user = UserAsResponse(
            id=new_user.id,
            email=new_user.email,
            username=new_user.username,
            created_at=new_user.created_at,
        )
        return new_user

    async def validate_user(self, user: UserLogin) -> AuthUser:
        """
        Validate the user credentials.

        Args:
            user (UserLogin): Pydantic model representing the user to login.

        Returns:
            AuthUser: Pydantic model representing the authenticated user.
        """
        unauthenticated_exception = HTTPException(
            status_code=401, detail="Could not validate credentials"
        )

        user_from_db = await self.repo.get_one(username=user.username)

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


class TokenService:
    def __init__(self, repo: Type[AbstractRepository[RefreshToken]]):
        self.repo = repo()

    async def create_access_token_and_refresh_token(self, user: AuthUser) -> Tokens:
        """
        Create an access token and a refresh token for the authenticated user.

        Args:
            user (AuthUser): Pydantic model representing the authenticated user.

        Returns:
            Tokens: Pydantic model representing the access and refresh tokens.
        """
        access_token = await self._create_access_token(user.id)
        refresh_token_uuid = await self._create_refresh_token(user.id, user.fingerprint)

        return Tokens(access_token=access_token, refresh_token_uuid=refresh_token_uuid)

    async def renew_access_token_and_refresh_token(
        self, refresh_token_uuid: str, fingerprint: str
    ) -> Tokens:
        """
        Renew an access token and a refresh token.

        Args:
            refresh_token_uuid (str): The refresh token UUID to be renewed.
            fingerprint (str): The fingerprint of the device from which the refresh token was generated.

        Returns:
            Tokens: Pydantic model representing the access and refresh tokens.
        """
        refresh_token = await self.repo.get_one(refresh_token_uuid=refresh_token_uuid)

        if not refresh_token:
            raise HTTPException(status_code=401, detail="Refresh token not found")

        await self.repo.delete_one(refresh_token)

        if (
            refresh_token.exp < int(datetime.now(timezone.utc).timestamp())
            or refresh_token.fingerprint != fingerprint
        ):
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        access_token = await self._create_access_token(refresh_token.sub)
        new_refresh_token_uuid = await self._create_refresh_token(
            refresh_token.sub, refresh_token.fingerprint
        )

        return Tokens(
            access_token=access_token, refresh_token_uuid=new_refresh_token_uuid
        )

    async def _create_access_token(self, user_id: int) -> str:
        """
        Create an access token for the user.

        Args:
            user_id (int): The ID of the user for whom the access token is being created.

        Returns:
            str: The generated access token encoded in JWT.
        """
        iat = datetime.now(timezone.utc)
        exp = iat + timedelta(minutes=settings.token.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = encode_jwt(
            payload={
                "sub": user_id,
                "scopes": [],
                "iat": int(iat.timestamp()),
                "exp": int(exp.timestamp()),
            }
        )

        return access_token

    async def _create_refresh_token(self, user_id: int, fingerprint: str) -> str:
        """
        Create a refresh token for the user.

        Args:
            user_id (int): The user ID for whom the refresh token is being created.
            fingerprint (str): The fingerprint of the device from which the refresh token was generated.

        Returns:
            str: The generated refresh token UUID.
        """
        refresh_token_uuid = str(uuid.uuid4())
        iat = datetime.now(timezone.utc)
        exp = iat + timedelta(days=settings.token.REFRESH_TOKEN_EXPIRE_DAYS)
        payload = {
            "sub": user_id,
            "fingerprint": fingerprint,
            "refresh_token_uuid": refresh_token_uuid,
            "iat": int(iat.timestamp()),
            "exp": int(exp.timestamp()),
        }
        await self.repo.add_one(payload)

        return str(refresh_token_uuid)
