from typing import Any, Dict
import bcrypt
import jwt
from config import settings


def encode_jwt(
    payload: Dict[str, Any],
    private_key: str = settings.crypto.PRIVATE_KEY_PATH.read_text(),
    algorithm: str = settings.crypto.ALGORITHM,
) -> str:
    return jwt.encode(payload, private_key, algorithm)


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.crypto.PUBLIC_KEY_PATH.read_text(),
    algorithm: str = settings.crypto.ALGORITHM,
) -> Dict[str, Any] | None:
    try:
        return jwt.decode(token, public_key, algorithms=[algorithm])
    except jwt.DecodeError:
        return None


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    password_bytes = password.encode()
    return bcrypt.hashpw(password_bytes, salt).decode("utf-8")


def validate_password_hash(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode("utf-8"))
