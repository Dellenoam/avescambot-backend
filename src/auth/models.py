from datetime import datetime
from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    is_verified: Mapped[bool] = mapped_column(nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    sub: Mapped[int] = mapped_column(nullable=False)
    fingerprint: Mapped[str] = mapped_column(nullable=False)
    refresh_token_uuid: Mapped[str] = mapped_column(nullable=False)
    iat: Mapped[int] = mapped_column(nullable=False)
    exp: Mapped[int] = mapped_column(nullable=False)
