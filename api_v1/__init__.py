from fastapi import APIRouter

from .users.views import router as users_router

from .profile.views import router as profiles_router

from .posts.views import router as posts_router

router = APIRouter(prefix='/api_v1')

router.include_router(users_router)

router.include_router(profiles_router)

router.include_router(posts_router)