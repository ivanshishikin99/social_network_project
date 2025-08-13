from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from api_v1.comments.schemas import CommentCreate, CommentUpdatePartial, CommentUpdateFull
from core.models import Comment, Post


async def create_comment(user_id: int, post_id: int, comment_data: CommentCreate, session: AsyncSession) -> Comment:
    comment = Comment(**comment_data.model_dump())
    comment.user_id = user_id
    comment.post_id = post_id
    session.add(comment)
    await session.commit()
    await session.refresh(comment)
    return comment


async def get_comment_by_id(comment_id: int, session: AsyncSession) -> Comment | None:
    return await session.get(Comment, comment_id)


async def delete_comment(user_id: int, comment: Comment, session: AsyncSession):
    post = await session.get(Post, comment.post_id)
    print(user_id)
    print(post.user_id)
    if user_id == comment.user_id or user_id == post.user_id:
        await session.delete(comment)
        await session.commit()
        return {"Comment deleted successfully!"}


async def update_comment_partial(comment: Comment, new_comment: CommentUpdatePartial, session: AsyncSession) -> Comment:
    for k, v in new_comment.model_dump().items():
        if k:
            setattr(comment, k, v)
    await session.commit()
    return comment


async def update_comment_full(comment: Comment, new_comment: CommentUpdateFull, session: AsyncSession) -> Comment:
    for k, v in new_comment.model_dump().items():
        setattr(comment, k, v)
    await session.commit()
    return comment
