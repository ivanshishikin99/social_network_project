import uuid
from typing import Optional

import requests.cookies
from fastapi import HTTPException, status, Response, Cookie, Request
from jwt import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import User, VerificationToken, PasswordResetToken
from utils.jwt_helpers import encode_jwt, decode_jwt


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


def decode_token(token: str) -> dict | InvalidTokenError:
    try:
        jwt = decode_jwt(token=token)
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not logged in.")
    return jwt


async def generate_new_access_token(response: Response, refresh_token: str, session: AsyncSession) -> str:
    payload = decode_token(token=refresh_token)
    user = await session.get(User, payload.get("user_id"))
    access_token = create_access_token(user=user)
    refresh_token = create_refresh_token(user=user)
    response.set_cookie("access_token", access_token, httponly=True)
    response.set_cookie("refresh_token", refresh_token, httponly=True)
    return access_token


async def get_user_by_token(request: Request, response: Response, session: AsyncSession) -> User:
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    if access_token:
        payload = decode_token(token=access_token.encode("UTF-8"))
        user = await session.get(User, payload.get("user_id"))
        return user
    elif refresh_token:
        access_token = await generate_new_access_token(response=response,
                                  refresh_token=refresh_token.encode("UTF-8"),
                                  session=session)
        payload = decode_token(token=access_token)
        user = await session.get(User, payload.get("user_id"))
        return user
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not logged in!")


def generate_verification_code() -> uuid.UUID:
    return uuid.uuid4()


async def get_token_by_user_email(user_email: str, session: AsyncSession) -> VerificationToken:
    statement = select(VerificationToken).where(VerificationToken.user_email == user_email)
    token = await session.execute(statement)
    token = token.scalar_one()
    return token


async def get_password_reset_token_by_user_email(user_email: str, session: AsyncSession) -> PasswordResetToken:
    statement = select(PasswordResetToken).where(PasswordResetToken.user_email == user_email)
    token = await session.execute(statement)
    token = token.scalar_one()
    return token
