from abc import ABC, abstractmethod
from sqlalchemy import select
from database import async_session


class AbstractRepository(ABC):
    """
    An abstract base class defining the interface for repository operations.

    Abstract Methods:
        add_one: Adds a new entity to the repository.
        get_one: Retrieves a single entity based on specified criteria.
        delete_one: Deletes a specific entity from the repository.
    """
    @abstractmethod
    async def add_one(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def get_one(self, **kwargs):
        raise NotImplementedError
    
    @abstractmethod
    async def delete_one(self, obj_to_delete):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    """
    A concrete implementation of AbstractRepository using SQLAlchemy for database operations.

    Inherits:
        AbstractRepository: An abstract base class defining the repository interface.

    Attributes:
        model: The SQLAlchemy model representing the entity to be managed in the repository.
    """
    def __init__(self, model):
        """
        Initializes the repository with the specified SQLAlchemy model.

        Args:
            model: The SQLAlchemy model representing the entity.
        """
        self.model = model

    async def add_one(self, data: dict):
        """
        Adds a new entity to the database.

        Args:
            data: A dictionary containing the data for the new entity.

        Returns:
            The newly created entity.
        """
        async with async_session() as session:
            new_obj = self.model(**data)
            session.add(new_obj)
            await session.commit()
            await session.refresh(new_obj)
            return new_obj

    async def get_one(self, **kwargs):
        """
        Retrieves a single entity based on the specified criteria.

        Args:
            kwargs: Keyword arguments representing the criteria for retrieval.

        Returns:
            The retrieved entity or None if not found.
        """
        async with async_session() as session:
            statement = select(self.model).filter_by(**kwargs).limit(1)
            result = await session.execute(statement)
            return result.scalar_one_or_none()
    
    async def delete_one(self, obj_to_delete):
        """
        Deletes a specific entity from the database.

        Args:
            obj_to_delete: The entity to be deleted.
        """
        async with async_session() as session:
            await session.delete(obj_to_delete)
            await session.commit()
