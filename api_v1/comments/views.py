from fastapi import APIRouter, status, Request, Response, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.comments.crud import create_comment
from api_v1.comments.schemas import CommentRead, CommentCreate
from core.models import Comment
from utils.db_helper import db_helper
from utils.token_helpers import get_user_by_token

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post("/create_comment", status_code=status.HTTP_200_OK, response_model=CommentRead)
async def create_comment_view(request: Request, response: Response,
                              comment_data: CommentCreate, post_id: int,
                              session: AsyncSession = Depends(db_helper.session_getter)) -> Comment:
    user = await get_user_by_token(request=request, response=response,
                                   session=session)
    return await create_comment(comment_data=comment_data, post_id=post_id, user_id=user.id,
                                session=session)
