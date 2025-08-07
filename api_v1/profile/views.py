from fastapi import APIRouter, status, Depends, Response, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.profile.crud import get_profile_by_user_id, update_user_profile_partial, update_user_profile_full
from api_v1.profile.schemas import ProfileRead, ProfileUpdatePartial, ProfileUpdateFull
from core.models import Profile, User
from utils.db_helper import db_helper
from utils.token_helpers import get_user_by_token

router = APIRouter(prefix="/profile")


@router.get('/user_profile', response_model=ProfileRead, status_code=status.HTTP_200_OK)
async def get_user_profile_view(request: Request, response: Response, session: AsyncSession = Depends(db_helper.session_getter)) -> Profile:
    user = await get_user_by_token(response=response, session=session, request=request)
    return await get_profile_by_user_id(user_id=user.id, session=session)

@router.patch("/update_user_profile_partial", response_model=ProfileRead, status_code=status.HTTP_200_OK)
async def update_user_profile_partial_view(profile_data: ProfileUpdatePartial, request: Request,
                                           response: Response, session: AsyncSession = Depends(db_helper.session_getter)) -> Profile | HTTPException:
    user = await get_user_by_token(response=response, session=session, request=request)
    profile = await get_profile_by_user_id(user_id=user.id, session=session)
    return await update_user_profile_partial(profile=profile, profile_data=profile_data, session=session)


@router.put("/update_user_profile_full", response_model=ProfileRead, status_code=status.HTTP_200_OK)
async def update_user_profile_full_view(profile_data: ProfileUpdateFull, request: Request,
                                        response: Response, session: AsyncSession = Depends(db_helper.session_getter)) -> Profile:
    user = await get_user_by_token(response=response, session=session, request=request)
    profile = await get_profile_by_user_id(user_id=user.id, session=session)
    return await update_user_profile_full(profile=profile, profile_data=profile_data, session=session)