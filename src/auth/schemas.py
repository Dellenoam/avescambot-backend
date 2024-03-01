from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    username: str
    password: str


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
