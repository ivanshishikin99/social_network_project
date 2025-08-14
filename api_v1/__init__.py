from fastapi import APIRouter

from .users.views import router as users_router

from .profile.views import router as profiles_router

from .posts.views import router as posts_router

from .comments.views import router as comments_router

from .messages.views import router as messages_router

router = APIRouter(prefix='/api_v1')

router.include_router(users_router)

router.include_router(profiles_router)

router.include_router(posts_router)

router.include_router(comments_router)

router.include_router(messages_router)