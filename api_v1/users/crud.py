import uuid

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.users.schemas import UserCreate
from core.models import User, Profile
from utils.password_helpers import hash_password, verify_password, validate_password
from utils.token_helpers import get_password_reset_token_by_user_email


async def create_user(user_data: UserCreate, session: AsyncSession) -> User:
    user_data.password = hash_password(password=user_data.password)
    user = User(**user_data.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    profile = Profile(user_id=user.id, is_public=True)
    session.add(profile)
    await session.commit()
    await session.refresh(profile)
    return user

async def login_user(username: str, password: str, session: AsyncSession) -> User:
    statement = select(User).where(User.username == username)
    user = await session.execute(statement)
    user = user.scalar_one()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wrong username.")
    if not verify_password(password=password,
                           hashed_password=user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong password.")
    return user


async def get_user_by_id(user_id: int, session: AsyncSession) -> User | None:
    return await session.get(User, user_id)


async def get_user_by_email(user_email: str, session: AsyncSession) -> User | None:
    statement = select(User).where(User.email == user_email)
    user = await session.execute(statement)
    user = user.scalar_one()
    return user


async def delete_user(user: User, session: AsyncSession):
    await session.delete(user)
    await session.commit()
    return "Your account has successfully been deleted!"


async def change_password(password: str, new_password: str, user: User, session: AsyncSession) -> User:
    if verify_password(password, user.password):
        if validate_password(cls=None, val=new_password):
            user.password = hash_password(new_password)
            await session.commit()
            await session.refresh(user)
            return user
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong password")


async def verify_password_reset_token(new_password: str, user_email: str, password_reset_token: uuid.UUID,
                                      session: AsyncSession, user: User):
    token = await get_password_reset_token_by_user_email(user_email=user_email, session=session)
    if not password_reset_token == token.token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong code.")
    if validate_password(cls=None, val=new_password):
        user.password = hash_password(password=new_password)
        await session.commit()
        await session.refresh(user)
    return "Your password has been changed!"
