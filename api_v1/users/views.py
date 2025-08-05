from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.users.crud import create_user
from api_v1.users.schemas import UserCreate
from utils.db_helper import db_helper

router = APIRouter(prefix='/users')

@router.post('/create_user')
async def register_user_view(user_data: UserCreate, session: AsyncSession = Depends(db_helper.session_getter)):
    return await create_user(user_data=user_data, session=session)