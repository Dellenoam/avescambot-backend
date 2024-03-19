from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, Optional, Sequence, Type, TypeVar
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import Base

ModelType = TypeVar("ModelType", bound=Base)


class AbstractRepository(ABC, Generic[ModelType]):
    """
    An abstract base class defining the interface for repository operations.

    Abstract Methods:
        add: Adds a new entity to the repository.
        get_by: Retrieves a single entity based on specified criteria.
        get_multiple_by: Retrieves multiple entities based on specified criteria.
        update: Updates an existing entity in the repository.
        delete: Deletes a specific entity from the repository.
    """

    @abstractmethod
    async def add(self, data: Dict[str, Any]) -> ModelType:
        raise NotImplementedError

    @abstractmethod
    async def get_by(self, **kwargs: Any) -> Optional[ModelType]:
        raise NotImplementedError

    @abstractmethod
    async def get_multiple_by(self, **kwargs: Any) -> Sequence[ModelType]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, obj_to_update: ModelType, data: Dict[str, Any]) -> ModelType:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, obj_to_delete: ModelType) -> None:
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository[ModelType]):
    """
    A concrete implementation of AbstractRepository using SQLAlchemy for database operations.
    """

    def __init__(self, session: AsyncSession, model_cls: Type[ModelType]):
        """
        Initializes the repository with the specified SQLAlchemy model.

        Args:
            session: The SQLAlchemy session to use for database operations.
            model_cls: The SQLAlchemy model class to use for the repository.
        """
        self._session = session
        self._model_cls = model_cls

    async def add(self, data: Dict[str, Any]) -> ModelType:
        """
        Adds a new entity to the database.

        Args:
            data: A dictionary containing the data for the new entity.

        Returns:
            The newly created entity.
        """
        new_obj = self._model_cls(**data)
        self._session.add(new_obj)
        await self._session.flush()
        return new_obj

    async def get_by(self, **filters: Any) -> ModelType | None:
        """
        Retrieves a single entity based on the specified criteria.

        Args:
            filters: Keyword arguments representing the criteria for retrieval.

        Returns:
            The retrieved entity or None if not found.
        """
        statement = select(self._model_cls).filter_by(**filters).limit(1)
        result = await self._session.execute(statement)
        return result.scalar_one_or_none()

    async def get_multiple_by(self, **filters: Any) -> Sequence[ModelType]:
        """
        Retrieves multiple entities based on the specified criteria.

        Args:
            filters: Keyword arguments representing the criteria for retrieval.

        Returns:
            A sequence of retrieved entities.
        """
        statement = select(self._model_cls).filter_by(**filters)
        result = await self._session.execute(statement)
        return result.scalars().all()

    async def update(self, obj_to_update: ModelType, data: Dict[str, Any]) -> ModelType:
        """
        Updates an existing entity in the database.

        Args:
            obj_to_update: The entity to be updated.
            data: A dictionary containing the updated data.

        Returns:
            The updated entity.
        """
        for key, value in data.items():
            setattr(obj_to_update, key, value)
        self._session.add(obj_to_update)
        await self._session.flush()
        return obj_to_update

    async def delete(self, obj_to_delete: ModelType) -> None:
        """
        Deletes a specific entity from the database.

        Args:
            obj_to_delete: The entity to be deleted.
        """
        await self._session.delete(obj_to_delete)
