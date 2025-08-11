import uuid
from datetime import timedelta, datetime
from typing import Optional

from fastapi import APIRouter, Depends, status, Response, Cookie, HTTPException, Request
from pydantic import SecretStr
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.users.crud import create_user, login_user, delete_user, change_password
from api_v1.users.dependencies import get_user_by_id_dependency
from api_v1.users.schemas import UserCreate, UserRead
from core.models import User, VerificationToken, PasswordResetToken
from utils.db_helper import db_helper
from utils.token_helpers import create_access_token, create_refresh_token, get_user_by_token, \
    generate_verification_code, get_token_by_user_email
from tasks.tasks import send_verification_email
from tasks import send_welcome_email

router = APIRouter(prefix='/users', tags=["Users"])

@router.get("/user", response_model=UserRead, status_code=status.HTTP_200_OK)
async def get_user_by_id(user_id: int, session: AsyncSession = Depends(db_helper.session_getter),
                         user: User = Depends(get_user_by_id_dependency)) -> User | HTTPException:
    return user


@router.post('/register_user', status_code=status.HTTP_200_OK)
async def register_user_view(user_data: UserCreate, session: AsyncSession = Depends(db_helper.session_getter)):
    user = await create_user(user_data=user_data, session=session)
    if user.email:
        send_welcome_email.delay(username=user.username, email=user.email, user_id=user.id)
        return {"You have registered successfully!"}


@router.post('/login_user', status_code=status.HTTP_200_OK)
async def login_user_view(response: Response, username: str, password: SecretStr,
                          session: AsyncSession = Depends(db_helper.session_getter)):
    user = await login_user(username=username,
                            password=password.get_secret_value(),
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


@router.delete("/delete_user", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_view(response: Response, request: Request, session: AsyncSession = Depends(db_helper.session_getter)):
    user = await get_user_by_token(request=request, response=response, session=session)
    return await delete_user(user=user, session=session)


@router.get("/send_email_verification_code", status_code=status.HTTP_200_OK)
async def send_verification_code_view(response: Response, request: Request, session: AsyncSession = Depends(db_helper.session_getter)):
    user = await get_user_by_token(request=request, response=response, session=session)
    verification_code = generate_verification_code()
    verification_token = VerificationToken(user_email=user.email,
                                           token=verification_code)
    session.add(verification_token)
    await session.commit()
    send_verification_email.delay(user_id=user.id, user_email=user.email, verification_code=verification_code)
    return {"Verification code has been sent. Please check your e-mail."}


@router.post("/verify_email", status_code=status.HTTP_200_OK)
async def verify_email_view(verification_code: uuid.UUID,
                            response: Response, request: Request,
                            session: AsyncSession = Depends(db_helper.session_getter)):
    user = await get_user_by_token(request=request, response=response, session=session)
    token = await get_token_by_user_email(user_email=user.email, session=session)
    print(token.token == verification_code)
    if token.token == verification_code:
        user.verified = True
        user.role_access = "Verified user"
        await session.commit()
        return {"Your email has been verified successfully!"}
    return {"Wrong code."}


@router.post("/change_password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password_view(password: SecretStr, new_password: SecretStr, request: Request, response: Response,
                               session: AsyncSession = Depends(db_helper.session_getter)):
    user = await get_user_by_token(request=request, response=response, session=session)
    return await change_password(password=password.get_secret_value(), new_password=new_password.get_secret_value(),
                                 user=user, session=session)

@router.post("/send_password_reset_token", status_code=status.HTTP_200_OK)
async def send_password_reset_token(user_email: str, session: AsyncSession = Depends(db_helper.session_getter)):
    token = generate_verification_code()
    password_reset_token = PasswordResetToken(user_email=user_email,
                                              token=token)
    session.add(password_reset_token)
    await session.commit()
    return {"A secret code has been sent, please check your email."}




