from auth.repository import RefreshTokenRepository, UserRepository
from auth.services import TokenService, AuthService


def auth_service() -> AuthService:
    return AuthService(UserRepository())


def token_service() -> TokenService:
    return TokenService(RefreshTokenRepository())
