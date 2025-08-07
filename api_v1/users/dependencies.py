from fastapi import HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User
from utils.db_helper import db_helper
from .crud import get_user_by_id


async def get_user_by_id_dependency(user_id: int, session: AsyncSession = Depends(db_helper.session_getter)) -> User | HTTPException:
    try:
        user = await get_user_by_id(user_id=user_id, session=session)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user