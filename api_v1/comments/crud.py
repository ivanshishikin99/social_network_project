from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.comments.schemas import CommentCreate
from core.models import Comment


async def create_comment(user_id: int, post_id: int, comment_data: CommentCreate, session: AsyncSession) -> Comment:
    comment = Comment(**comment_data.model_dump())
    comment.user_id = user_id
    comment.post_id = post_id
    session.add(comment)
    await session.commit()
    await session.refresh(comment)
    return comment
