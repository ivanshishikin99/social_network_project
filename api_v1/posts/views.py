from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import Response

from api_v1.posts.crud import create_post, delete_post
from api_v1.posts.dependencies import get_post_by_id_dependency
from api_v1.posts.schemas import PostCreate, PostRead
from core.models import Post
from utils.db_helper import db_helper
from utils.token_helpers import get_user_by_token

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("/create_post", response_model=PostRead, status_code=status.HTTP_200_OK)
async def create_post_view(request: Request, response: Response, post_data: PostCreate,
                           session: AsyncSession = Depends(db_helper.session_getter)) -> Post:
    user = await get_user_by_token(request=request, response=response, session=session)
    return await create_post(post_data=post_data, session=session, user=user)


@router.get("/get_post_by_id", response_model=PostRead, status_code=status.HTTP_200_OK)
async def get_post_by_id_view(post_id: int, session: AsyncSession = Depends(db_helper.session_getter),
                              post: Post = Depends(get_post_by_id_dependency)) -> Post:
    return post


@router.delete("/delete_post", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post_view(request: Request, response: Response, post_id: int,
                      session: AsyncSession = Depends(db_helper.session_getter),
                      post: Post = Depends(get_post_by_id_dependency)):
    user = await get_user_by_token(request=request, response=response, session=session)
    return await delete_post(post=post, session=session, user_id=user.id)

