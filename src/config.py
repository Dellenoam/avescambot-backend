from pathlib import Path
from pydantic import PositiveInt
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent


class DBSettings(BaseSettings):
    DB_URL: str

class CryptoSettings(BaseSettings):
    PRIVATE_KEY_PATH: Path = BASE_DIR / "certs" / "private.pem"
    PUBLIC_KEY_PATH: Path = BASE_DIR / "certs" / "public.pem"
    ALGORITHM: str = "RS256"

class TokenSettings(BaseSettings):
    ACCESS_TOKEN_EXPIRE_MINUTES: PositiveInt = 7
    REFRESH_TOKEN_EXPIRE_DAYS: PositiveInt = 7

class CookieSettings(BaseSettings):
    COOKIE_SECURE_FLAG: bool 
    COOKIE_PATHS: str = "/api/auth/refresh"

class Settings(BaseSettings):
    db: DBSettings = DBSettings() # type: ignore
    crypto: CryptoSettings = CryptoSettings()
    token: TokenSettings = TokenSettings()
    cookie: CookieSettings = CookieSettings() # type: ignore

    model_config = SettingsConfigDict(env_file='.env')

settings = Settings()
