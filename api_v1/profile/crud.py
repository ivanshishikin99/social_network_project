from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.profile.schemas import ProfileUpdatePartial, ProfileUpdateFull
from core.models import Profile, User


async def get_profile_by_user_id(user_id: int, session: AsyncSession) -> Profile:
    statement = select(Profile).where(Profile.user_id==user_id)
    profile = await session.execute(statement)
    profile = profile.scalar_one()
    return profile


async def get_profile_by_profile_id(profile_id: int, session: AsyncSession) -> Profile | None:
    return await session.get(Profile, profile_id)


async def get_user_by_profile(profile: Profile, session: AsyncSession) -> User | None:
    return await session.get(User, profile.user_id)


async def update_user_profile_partial(profile: Profile, profile_data: ProfileUpdatePartial, session: AsyncSession) -> Profile:
    for k, v in profile_data.model_dump().items():
        if k:
            setattr(profile, k, v)
    await session.commit()
    await session.refresh(profile)
    return profile


async def update_user_profile_full(profile: Profile, profile_data: ProfileUpdateFull, session: AsyncSession) -> Profile:
    for k, v in profile_data.model_dump().items():
        setattr(profile, k, v)
    await session.commit()
    await session.refresh(profile)
    return profile
