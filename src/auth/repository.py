from auth.models import RefreshToken, User
from repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    """
    Repository for handling operations related to users.

    Inherits:
        SQLAlchemyRepository: A base repository class providing common database operations.
    """
    def __init__(self):
        super().__init__(model=User)


class RefreshSessionRepository(SQLAlchemyRepository):
    """
    Repository for handling operations related to refresh tokens.

    Inherits:
        SQLAlchemyRepository: A base repository class providing common database operations.
    """
    def __init__(self):
        super().__init__(model=RefreshToken)
