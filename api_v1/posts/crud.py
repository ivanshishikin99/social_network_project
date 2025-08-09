from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.posts.schemas import PostCreate
from core.models import Post, User


async def create_post(post_data: PostCreate, session: AsyncSession, user: User) -> Post:
    post = Post(**post_data.model_dump())
    post.user_id = user.id
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post
