import bcrypt


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt(rounds=12)
    encoded = password.encode()
    return bcrypt.hashpw(password=encoded, salt=salt)


def verify_password(password: str, hashed_password: bytes) -> bool:
    encoded = password.encode()
    return bcrypt.checkpw(password=encoded, hashed_password=hashed_password)

