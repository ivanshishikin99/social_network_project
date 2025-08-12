from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.comments.crud import get_comment_by_id
from core.models import Comment
from utils.db_helper import db_helper


async def get_comment_by_id_dependency(comment_id: int, session: AsyncSession = Depends(db_helper.session_getter)) -> Comment | HTTPException:
    try:
        comment = await get_comment_by_id(comment_id=comment_id, session=session)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found.")
    return comment