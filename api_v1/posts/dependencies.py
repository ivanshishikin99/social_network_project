from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.posts.crud import get_post_by_id
from core.models import Post
from utils.db_helper import db_helper


async def get_post_by_id_dependency(post_id: int, session: AsyncSession = Depends(db_helper.session_getter)) -> Post | HTTPException:
    try:
        post = await get_post_by_id(post_id=post_id, session=session)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found.")
    return post
