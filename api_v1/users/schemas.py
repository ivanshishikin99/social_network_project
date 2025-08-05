from pydantic import BaseModel, EmailStr, field_validator

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
    def validate_password(cls, val: str) -> str | ValueError:
        if len(val) < 8:
            raise ValueError("Your password must include at least 8 characters.")
        if len(val) > 100:
            raise ValueError("Your password must not exceed 100 characters.")
        special_symbols_flag = False
        digits_flag = False
        upper_character_flag = False
        for i in val:
            if i in special_symbols:
                special_symbols_flag = True
            if i.isdigit():
                digits_flag = True
            if i.isupper():
                upper_character_flag = True
        if not special_symbols_flag:
            raise ValueError("Your password must include at least one special character.")
        if not digits_flag:
            raise ValueError("Your password must include at least one digit.")
        if not upper_character_flag:
            raise ValueError("Your password must include at least one upper character.")
        return val

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


