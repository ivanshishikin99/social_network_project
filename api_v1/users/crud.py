from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.users.schemas import UserCreate
from core.models import User, Profile


async def create_user(user_data: UserCreate, session: AsyncSession) -> User:
    user = User(**user_data.model_dump())
    profile = Profile()
    profile.user_id = user.id
    session.add(user)
    session.add(profile)
    await session.commit()
    await session.refresh(user)
    await session.refresh(profile)
    return user