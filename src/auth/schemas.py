from datetime import datetime
import re
from pydantic import BaseModel, EmailStr, Field, validator


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    username: str
    password: str = Field(min_length=8, max_length=64, examples=["StrongPassword123!"])

    @validator("password")
    def validate_password_complexity(cls, password: str) -> str:
        if not re.search("[a-z]", password) or not re.search("[A-Z]", password):
            raise ValueError(
                "Password must contain at least one uppercase letter and one lowercase letter"
            )
        if not re.search("[0-9]", password):
            raise ValueError("Password must contain at least one digit")
        if not re.search("[!@#$%^&*()_+{}:<>?]", password):
            raise ValueError("Password must contain at least one special character")

        return password


class UserLogin(UserBase):
    password: str
    fingerprint: str


class UserAsResponse(UserBase):
    id: int
    username: str
    created_at: datetime


class AuthUser(UserAsResponse):
    fingerprint: str


class AccessToken(BaseModel):
    access_token: str


class RefreshSessionInput(BaseModel):
    fingerprint: str
