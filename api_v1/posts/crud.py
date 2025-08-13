from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.posts.schemas import PostCreate, PostUpdatePartial, PostUpdateFull
from core.models import Post, User, Comment


async def create_post(post_data: PostCreate, session: AsyncSession, user: User) -> Post:
    post = Post(**post_data.model_dump())
    post.user_id = user.id
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post


async def get_post_by_id(post_id: int, session: AsyncSession) -> Post | None:
    return await session.get(Post, post_id)


async def delete_post(post: Post, session: AsyncSession, user_id: int):
    if user_id == post.user_id:
        await session.delete(post)
        await session.commit()
        return "Post successfully deleted"


async def update_post_partial(post: Post, post_data: PostUpdatePartial, session: AsyncSession, user_id: int) -> Post:
    if user_id == post.user_id:
        for k, v in post_data.model_dump().items():
            if k:
                setattr(post, k, v)
        await session.commit()
        return post


async def update_post_full(post: Post, post_data: PostUpdateFull, session: AsyncSession, user_id: int) -> Post:
    if user_id == post.user_id:
        for k, v in post_data.model_dump().items():
            setattr(post, k, v)
        await session.commit()
        return post


async def get_comments_by_post_id(post_id: int, session: AsyncSession) -> Sequence[Comment]:
    statement = select(Comment).where(Comment.post_id == post_id)
    comments = await session.execute(statement)
    comments = comments.scalars().all()
    return comments


async def get_posts_by_user_id(user_id: int, session: AsyncSession) -> Sequence[Post]:
    statement = select(Post).where(Post.user_id == user_id)
    posts = await session.execute(statement)
    posts = posts.scalars().all()
    return posts

