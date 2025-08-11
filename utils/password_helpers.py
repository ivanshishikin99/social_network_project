from typing import Type, TYPE_CHECKING

import bcrypt


if TYPE_CHECKING:
    from api_v1.users.schemas import UserCreate


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt(rounds=12)
    encoded = password.encode()
    return bcrypt.hashpw(password=encoded, salt=salt)


def verify_password(password: str, hashed_password: bytes) -> bool:
    encoded = password.encode()
    return bcrypt.checkpw(password=encoded, hashed_password=hashed_password)


def validate_password(cls: Type["UserCreate"] | None, val: str) -> str | ValueError:
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
