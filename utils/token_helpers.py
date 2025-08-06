from fastapi import HTTPException, status

from core.config import settings
from core.models import User
from utils.jwt_helpers import encode_jwt


def create_token(payload: dict,
                 token_type: str):
    jwt_payload = {"type": token_type}
    if token_type == "access":
        expire_minutes: int = settings.jwt_config.access_token_expire_minutes
    elif token_type == "refresh":
        expire_minutes: int = settings.jwt_config.refresh_token_expire_minutes
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type.")
    jwt_payload.update(payload)
    return encode_jwt(payload=jwt_payload,
                      expire_minutes=expire_minutes)


def create_access_token(user: User):
    jwt_payload = {"sub": user.username,
                   "user_id": user.id,
                   "email": user.email,
                   "role_access": user.role_access,
                   "verified": user.verified}
    return create_token(payload=jwt_payload,
                        token_type="access")


def create_refresh_token(user: User):
    jwt_payload = {"sub": user.username,
                   "user_id": user.id,
                   "email": user.email}
    return create_token(payload=jwt_payload,
                        token_type="refresh")