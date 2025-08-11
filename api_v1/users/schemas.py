from pydantic import BaseModel, EmailStr, field_validator

from utils.password_helpers import validate_password

unacceptable_words = []

special_symbols = [
            "@", "#", "$", "%",
            "&", "!", "?", "[",
            "]", "(", ")", "£",
            "€", "¥", "<", ">",
            "{", "}", "+", "-",
            "=", "\\", "/", ",",
            ".", ":", ";", "`",
            "#", "^", "*",
        ]

class UserCreate(BaseModel):
    username: str
    password: str
    verified: bool = False
    role_access: str = "Unverified user"
    email: EmailStr

    @field_validator("username")
    @classmethod
    def validate_username(cls, val: str) -> str | ValueError:
        if len(val) <= 2:
            raise ValueError("Your username must include at least 3 characters.")
        if len(val) >= 30:
            raise ValueError("Your username must not exceed 30 characters.")
        for i in unacceptable_words:
            if i in val:
                raise ValueError("Your username includes unacceptable words.")
        return val

    @field_validator("password")
    @classmethod
    def validate_model_password(cls, val: str) -> str | ValueError:
        return validate_password(cls=cls, val=val)

    @field_validator("verified")
    @classmethod
    def validate_verification(cls, val: bool) -> bool | ValueError:
        if val is True:
            raise ValueError("Incorrect verified value.")
        return val

    @field_validator("role_access")
    @classmethod
    def validate_role_access(cls, val: str) -> str | ValueError:
        if not val == "Unverified user":
            raise ValueError("Incorrect role access.")
        return val


class UserRead(BaseModel):
    username: str
    verified: bool
    role_access: str
    email: EmailStr


