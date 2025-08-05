from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.users.schemas import UserCreate
from core.models import User, Profile
from utils.password_helpers import hash_password


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