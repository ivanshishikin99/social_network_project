from typing import Optional

from fastapi import APIRouter, Depends, status, Response, Cookie
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.users.crud import create_user, login_user
from api_v1.users.schemas import UserCreate
from utils.db_helper import db_helper
from utils.token_helpers import create_access_token, create_refresh_token
from utils.token_model import TokenModel

router = APIRouter(prefix='/users')

@router.post('/create_user')
async def register_user_view(user_data: UserCreate, session: AsyncSession = Depends(db_helper.session_getter)):
    return await create_user(user_data=user_data, session=session)


@router.get('/login_user', response_model=TokenModel, status_code=status.HTTP_200_OK)
async def login_user_view(response: Response, username: str, password: str, session: AsyncSession = Depends(db_helper.session_getter)) -> TokenModel:
    user = await login_user(username=username,
                            password=password,
                            session=session)
    access_token = create_access_token(user=user)
    refresh_token = create_refresh_token(user=user)
    response.set_cookie("access_token", access_token, httponly=True)
    response.set_cookie("refresh_token", refresh_token, httponly=True)
    return TokenModel(access_token=access_token,
                      refresh_token=refresh_token)

@router.get('/logout_user')
async def logout_user_view(response: Response, access_token: Optional[str] = Cookie(None),
                           refresh_token: Optional[str] = Cookie(None)):
    if access_token or refresh_token:
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return {"You have logged out successfully!"}
    else:
        return {"You are not logged in."}
