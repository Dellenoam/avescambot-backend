from datetime import datetime
from uuid import UUID
from fastapi import HTTPException
from sqlalchemy import select
from .utils import hash_password
from .models import RefreshSession, User
from .schemas import UserAsResponse, UserCreate
from src.database import session


class AuthRepository:
    def __init__(self):
        self._user_model = User
        self._refresh_session_model = RefreshSession
        self._session = session

    async def create_user(self, new_user: UserCreate) -> UserAsResponse:  # type: ignore
        async with self._session() as session:
            if await self.get_user_by_email(new_user.email):
                raise HTTPException(status_code=409, detail="User already exists")

            new_user_object = self._user_model(
                username=new_user.username,
                email=new_user.email,
                hashed_password=hash_password(new_user.password),
            )

            session.add(new_user_object)

            await session.commit()

            await session.refresh(new_user_object)

            return UserAsResponse(
                id=new_user_object.id,
                username=new_user_object.username,
                email=new_user_object.email,
                created_at=new_user_object.created_at,
            )

    async def create_refresh_session(
        self,
        sub: int,
        fingerprint: str,
        refresh_session_uuid: str,
        iat: datetime,
        exp: datetime,
    ) -> None:
        async with self._session() as session:
            new_refresh_session = self._refresh_session_model(
                sub=sub,
                fingerprint=fingerprint,
                refresh_session_uuid=refresh_session_uuid,
                iat=iat,
                exp=exp,
            )

            session.add(new_refresh_session)

            await session.commit()

    async def get_refresh_session_by_refresh_session_uuid(
        self, refresh_session_uuid: str
    ) -> RefreshSession | None:
        async with self._session() as session:
            query = select(self._refresh_session_model).filter(
                self._refresh_session_model.refresh_session_uuid == refresh_session_uuid
            )
            result = await session.execute(query)
            refresh_session = result.scalars().first()

            return refresh_session

    async def get_user_by_email(self, email: str) -> User | None:
        async with self._session() as session:
            query = select(self._user_model).filter(self._user_model.email == email)
            result = await session.execute(query)

            user = result.scalars().first()
            return user

    async def delete_refresh_session(self, refresh_session: RefreshSession) -> None:
        async with self._session() as session:
            await session.delete(refresh_session)
