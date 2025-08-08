from typing import Optional

from fastapi import APIRouter, Depends, status, Response, Cookie, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.users.crud import create_user, login_user
from api_v1.users.dependencies import get_user_by_id_dependency
from api_v1.users.schemas import UserCreate, UserRead
from core.models import User
from mailing.email_senders import send_welcome_email
from utils.db_helper import db_helper
from utils.token_helpers import create_access_token, create_refresh_token
from utils.token_model import TokenModel

router = APIRouter(prefix='/users', tags=["Users"])

@router.get("/user", response_model=UserRead, status_code=status.HTTP_200_OK)
async def get_user_by_id(user_id: int, session: AsyncSession = Depends(db_helper.session_getter),
                         user: User = Depends(get_user_by_id_dependency)) -> User | HTTPException:
    return user


@router.post('/register_user', status_code=status.HTTP_200_OK)
async def register_user_view(user_data: UserCreate, session: AsyncSession = Depends(db_helper.session_getter)):
    user = await create_user(user_data=user_data, session=session)
    send_welcome_email(username=user.username, email=user.email)
    return {"You have registered successfully!"}


@router.post('/login_user', status_code=status.HTTP_200_OK)
async def login_user_view(response: Response, username: str, password: str,
                          session: AsyncSession = Depends(db_helper.session_getter)):
    user = await login_user(username=username,
                            password=password,
                            session=session)
    access_token = create_access_token(user=user)
    refresh_token = create_refresh_token(user=user)
    response.set_cookie("access_token", access_token, httponly=True)
    response.set_cookie("refresh_token", refresh_token, httponly=True)
    return "You have logged in successfully!"

@router.get('/logout_user')
async def logout_user_view(response: Response, access_token: Optional[str] = Cookie(None),
                           refresh_token: Optional[str] = Cookie(None)):
    if access_token or refresh_token:
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return {"You have logged out successfully!"}
    else:
        return {"You are not logged in."}
