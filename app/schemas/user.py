import re
from pydantic import BaseModel, Field, EmailStr, model_validator
from typing_extensions import Self
from enum import Enum


class UserLogIn(BaseModel):
    email: EmailStr
    password1: str = Field(min_length=8, default="Z36sven3425Z%")


class UserCreate(UserLogIn):
    password2: str = Field(min_length=8)

    @model_validator(mode="after")
    def check_passwords(self) -> Self:
        pw1 = self.password1
        pw2 = self.password2

        if pw1 != pw2:
            raise ValueError("Passwords do not match")

        if len(pw1) < 8:
            raise ValueError("Password must be at least 8 characters long")

        if not re.fullmatch(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*]).+$", pw1
        ):
            raise ValueError(
                "Password must contain at least one lowercase letter, one uppercase letter, one digit, and one special character"
            )

        return self


class UserCreateOutput(BaseModel):
    email: EmailStr


class UserModel(BaseModel):
    email: EmailStr
    hash_password: str


class UserId(BaseModel):
    id: int


class Country(str, Enum):
    Russia = "Россия"


class City(str, Enum):
    SaintPeterburg = "Санкт-Петербург"


class UserAddress(BaseModel):
    country: Country
    city: City
    postal_code: int = 241517
    address_line: str
