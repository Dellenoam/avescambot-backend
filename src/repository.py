from abc import ABC, abstractmethod
from sqlalchemy import select
from database import async_session


class AbstractRepository(ABC):
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
    def __init__(self, model):
        self.model = model

    async def add_one(self, data: dict):
        async with async_session() as session:
            new_obj = self.model(**data)
            session.add(new_obj)
            await session.commit()
            await session.refresh(new_obj)
            return new_obj

    async def get_one(self, **kwargs):
        async with async_session() as session:
            statement = select(self.model).filter_by(**kwargs).limit(1)
            result = await session.execute(statement)
            return result.scalar_one_or_none()
    
    async def delete_one(self, obj_to_delete):
        async with async_session() as session:
            await session.delete(obj_to_delete)
            await session.commit()
