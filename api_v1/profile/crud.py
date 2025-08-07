from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Profile


async def get_profile_by_user_id(user_id: int, session: AsyncSession) -> Profile:
    statement = select(Profile).where(Profile.user_id==user_id)
    profile = await session.execute(statement)
    profile = profile.scalar_one()
    return profile
