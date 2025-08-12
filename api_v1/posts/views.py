from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import Response

from api_v1.posts.crud import create_post, delete_post, update_post_partial, update_post_full
from api_v1.posts.dependencies import get_post_by_id_dependency
from api_v1.posts.schemas import PostCreate, PostRead, PostUpdatePartial, PostUpdateFull
from core.models import Post
from utils.db_helper import db_helper
from utils.token_helpers import get_user_by_token

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("/post", response_model=PostRead, status_code=status.HTTP_200_OK)
async def create_post_view(request: Request, response: Response, post_data: PostCreate,
                           session: AsyncSession = Depends(db_helper.session_getter)) -> Post:
    user = await get_user_by_token(request=request, response=response, session=session)
    return await create_post(post_data=post_data, session=session, user=user)


@router.get("/post/{post_id}", response_model=PostRead, status_code=status.HTTP_200_OK)
async def get_post_by_id_view(post_id: int, session: AsyncSession = Depends(db_helper.session_getter),
                              post: Post = Depends(get_post_by_id_dependency)) -> Post:
    return post


@router.delete("/post/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post_view(request: Request, response: Response, post_id: int,
                      session: AsyncSession = Depends(db_helper.session_getter),
                      post: Post = Depends(get_post_by_id_dependency)):
    user = await get_user_by_token(request=request, response=response, session=session)
    return await delete_post(post=post, session=session, user_id=user.id)


@router.patch("/post/{post_id}", status_code=status.HTTP_200_OK, response_model=PostRead)
async def update_post_partial_view(request: Request, response: Response, post_id: int,
                                   post_data: PostUpdatePartial,
                                   session: AsyncSession = Depends(db_helper.session_getter),
                                   post: Post = Depends(get_post_by_id_dependency)) -> Post:
    user = await get_user_by_token(request=request, response=response, session=session)
    return await update_post_partial(post=post, post_data=post_data, user_id=user.id, session=session)


@router.put("/post/{post_id}", status_code=status.HTTP_200_OK, response_model=PostRead)
async def update_post_full_view(request: Request, response: Response, post_id: int,
                                post_data: PostUpdateFull,
                                session: AsyncSession = Depends(db_helper.session_getter),
                                post: Post = Depends(get_post_by_id_dependency)) -> Post:
    user = await get_user_by_token(request=request, response=response, session=session)
    return await update_post_full(post=post, post_data=post_data, user_id=user.id, session=session)

