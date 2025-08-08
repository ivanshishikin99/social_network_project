from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.profile.crud import get_profile_by_profile_id
from core.models import Profile
from utils.db_helper import db_helper


async def get_profile_by_profile_id_dependency(profile_id: int, session: AsyncSession = Depends(db_helper.session_getter)) -> Profile | HTTPException:
    try:
        profile = await get_profile_by_profile_id(profile_id=profile_id, session=session)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return profile
