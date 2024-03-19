from abc import ABC, abstractmethod
from typing import Self
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from auth.repository import RefreshTokenRepository, UserRepository


class AbstractUnitOfWork(ABC):
    @abstractmethod
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        raise NotImplementedError

    @property
    @abstractmethod
    def user(self) -> UserRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def refresh_token(self) -> RefreshTokenRepository:
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self) -> Self:
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, exc_type, exc_value, traceback) -> None:  # type: ignore
        raise NotImplementedError

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError


class UnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self._session_factory = session_factory
        self._user_repo = None
        self._refresh_token_repo = None

    @property
    def user(self) -> UserRepository:
        if self._user_repo is None:
            self._user_repo = UserRepository(session=self._session)
        return self._user_repo

    @property
    def refresh_token(self) -> RefreshTokenRepository:
        if self._refresh_token_repo is None:
            self._refresh_token_repo = RefreshTokenRepository(session=self._session)
        return self._refresh_token_repo

    async def __aenter__(self) -> Self:
        self._session = self._session_factory()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:  # type: ignore
        if exc_type is not None:
            await self.rollback()
        await self._session.close()

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()
