from auth.repository import RefreshSessionRepository, UserRepository
from auth.services import TokenService, AuthService


def auth_service() -> AuthService:
    return AuthService(UserRepository())


def token_service() -> TokenService:
    return TokenService(RefreshSessionRepository())
