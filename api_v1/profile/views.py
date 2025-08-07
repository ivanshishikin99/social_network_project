from fastapi import APIRouter, status, Depends, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.profile.crud import get_profile_by_user_id
from api_v1.profile.schemas import ProfileRead
from core.models import Profile, User
from utils.db_helper import db_helper
from utils.token_helpers import get_user_by_token

router = APIRouter(prefix="/profile")


@router.get('/user_profile', response_model=ProfileRead, status_code=status.HTTP_200_OK)
async def get_user_profile_view(request: Request, response: Response, session: AsyncSession = Depends(db_helper.session_getter)) -> Profile:
    user = await get_user_by_token(response=response, session=session, request=request)
    return await get_profile_by_user_id(user_id=user.id, session=session)