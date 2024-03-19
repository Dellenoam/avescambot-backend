from sqlalchemy.ext.asyncio import AsyncSession
from auth.models import RefreshToken, User
from repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository[User]):
    """
    Repository for handling operations related to users.

    Inherits:
        SQLAlchemyRepository: A base repository class providing common database operations.
    """

    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model_cls=User)


class RefreshTokenRepository(SQLAlchemyRepository[RefreshToken]):
    """
    Repository for handling operations related to refresh tokens.

    Inherits:
        SQLAlchemyRepository: A base repository class providing common database operations.
    """

    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model_cls=RefreshToken)
