from pathlib import Path
from pydantic import BaseModel, PositiveInt
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent


class DBSettings(BaseModel):
    URL: str


class CryptoSettings(BaseModel):
    PRIVATE_KEY_PATH: Path = BASE_DIR / "certs" / "private.pem"
    PUBLIC_KEY_PATH: Path = BASE_DIR / "certs" / "public.pem"
    ALGORITHM: str = "RS256"


class TokenSettings(BaseModel):
    ACCESS_TOKEN_EXPIRE_MINUTES: PositiveInt = 7
    REFRESH_TOKEN_EXPIRE_DAYS: PositiveInt = 7


class CookieSettings(BaseModel):
    SECURE_FLAG: bool
    PATHS: str = "/api/auth/refresh"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_nested_delimiter="__")
    db: DBSettings
    crypto: CryptoSettings = CryptoSettings()
    token: TokenSettings = TokenSettings()
    cookie: CookieSettings


settings = Settings()  # type: ignore
