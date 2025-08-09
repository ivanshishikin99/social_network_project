from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.posts.schemas import PostCreate, PostUpdatePartial
from core.models import Post, User


async def create_post(post_data: PostCreate, session: AsyncSession, user: User) -> Post:
    post = Post(**post_data.model_dump())
    post.user_id = user.id
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post


async def get_post_by_id(post_id: int, session: AsyncSession) -> Post | None:
    return await session.get(Post, post_id)


# async def update_post_partial(post: Post, post_data: PostUpdatePartial, session: AsyncSession) -> Post:
#     for k, v in post_data.model_dump().items():
#         if k:
#             setattr(post_data, k, v)
#     await session.commit()
#     return
