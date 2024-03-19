from auth.services import TokenService, AuthService
from unitofwork import UnitOfWork


def auth_service() -> AuthService:
    return AuthService(UnitOfWork)


def token_service() -> TokenService:
    return TokenService(UnitOfWork)
