from pathlib import Path
from pydantic import PositiveInt
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent


class DBSettings(BaseSettings):
    db_url: str

class CryptoSettings(BaseSettings):
    private_key_path: Path = BASE_DIR / "certs" / "private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "public.pem"
    algorithm: str = "RS256"

class TokenSettings(BaseSettings):
    access_token_expire_minutes: PositiveInt = 7
    refresh_session_expire_days: PositiveInt = 7

class CookieSettings(BaseSettings):
    cookie_secure_flag: bool = False
    cookie_paths: str = "/api/auth/refresh"

class Settings(BaseSettings):
    db: DBSettings = DBSettings() # type: ignore
    crypto: CryptoSettings = CryptoSettings()
    token: TokenSettings = TokenSettings()
    cookie: CookieSettings = CookieSettings()

    model_config = SettingsConfigDict(env_file='.env')

settings = Settings()
