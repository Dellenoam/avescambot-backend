from datetime import datetime
import re
from pydantic import BaseModel, EmailStr, Field, validator


class UserCreate(BaseModel):
    username: str = Field(min_length=4, max_length=20, examples=["username"])
    email: EmailStr
    password: str = Field(min_length=8, max_length=64, examples=["StrongPassword123!"])

    @validator("password")
    def validate_password_complexity(cls, password: str) -> str:
        """
        Validate the complexity of the password.

        Args:
            cls: The class.
            password (str): The password to be validated.

        Returns:
            str: The validated password.
        """
        if not re.search("[a-z]", password) or not re.search("[A-Z]", password):
            raise ValueError(
                "password must contain at least one uppercase letter and one lowercase letter"
            )

        if not re.search("[0-9]", password):
            raise ValueError("password must contain at least one digit")

        if not re.search("[!@#$%^&*()_+{}:<>?]", password):
            raise ValueError("password must contain at least one special character")

        return password


class UserLogin(BaseModel):
    username: str = Field(examples=["username"])
    password: str = Field(examples=["StrongPassword123!"])
    fingerprint: str = Field(examples=["user_browser_fingerprint"])


class UserAsResponse(BaseModel):
    id: int
    username: str = Field(examples=["username"])
    email: EmailStr
    created_at: datetime


class AuthUser(UserAsResponse):
    fingerprint: str = Field(examples=["user_browser_fingerprint"])


class Tokens(BaseModel):
    access_token: str = Field(examples=["access_token"])
    refresh_token_uuid: str = Field(examples=["refresh_token_uuid"])


class AccessToken(BaseModel):
    access_token: str = Field(examples=["access_token"])
    token_type: str = Field(default="bearer", examples=["bearer"])


class UserDetails(BaseModel):
    fingerprint: str = Field(examples=["user_browser_fingerprint"])
