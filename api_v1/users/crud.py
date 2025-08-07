from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.users.schemas import UserCreate
from core.models import User, Profile
from utils.password_helpers import hash_password, verify_password


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
