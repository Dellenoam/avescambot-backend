from auth.models import RefreshToken, User
from repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(model=User)


class RefreshSessionRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(model=RefreshToken)
