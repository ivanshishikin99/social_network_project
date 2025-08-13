from fastapi import APIRouter, status, Request, Response, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.comments.crud import create_comment, delete_comment, update_comment_partial, update_comment_full
from api_v1.comments.dependencies import get_comment_by_id_dependency
from api_v1.comments.schemas import CommentRead, CommentCreate, CommentUpdatePartial, CommentUpdateFull
from core.models import Comment
from utils.db_helper import db_helper
from utils.token_helpers import get_user_by_token

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post("/comment", status_code=status.HTTP_200_OK, response_model=CommentRead)
async def create_comment_view(request: Request, response: Response,
                              comment_data: CommentCreate, post_id: int,
                              session: AsyncSession = Depends(db_helper.session_getter)) -> Comment:
    user = await get_user_by_token(request=request, response=response,
                                   session=session)
    return await create_comment(comment_data=comment_data, post_id=post_id, user_id=user.id,
                                session=session)


@router.get("/comment/{comment_id}", status_code=status.HTTP_200_OK, response_model=CommentRead)
async def get_comment_by_id_view(comment_id: int, comment: Comment = Depends(get_comment_by_id_dependency)) -> Comment:
    return comment


@router.delete("/comment/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment_by_id_view(request: Request, response: Response,
                                    comment_id: int, comment: Comment = Depends(get_comment_by_id_dependency),
                                    session: AsyncSession = Depends(db_helper.session_getter)):
    user = await get_user_by_token(request=request, response=response, session=session)
    return await delete_comment(comment=comment, session=session, user_id=user.id)


@router.patch("/comment/{comment_id}", status_code=status.HTTP_200_OK, response_model=CommentRead)
async def update_comment_partial_view(request: Request, response: Response,
                                      comment_id: int, new_comment: CommentUpdatePartial,
                                      comment: Comment = Depends(get_comment_by_id_dependency),
                                      session: AsyncSession = Depends(db_helper.session_getter)) -> Comment:
    user = await get_user_by_token(request=request, response=response, session=session)
    if not comment.user_id == user.id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            detail="You are not authorized to change other users' comments.")
    return await update_comment_partial(comment=comment, new_comment=new_comment, session=session)


@router.put("/comment/{comment_id}", status_code=status.HTTP_200_OK, response_model=CommentRead)
async def update_comment_full_view(request: Request, response: Response,
                                   comment_id: int, new_comment: CommentUpdateFull,
                                   comment: Comment = Depends(get_comment_by_id_dependency),
                                   session: AsyncSession = Depends(db_helper.session_getter)) -> Comment:
    user = await get_user_by_token(request=request, response=response, session=session)
    if not comment.user_id == user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="You are not authorized to change other users' comments.")
    return await update_comment_full(comment=comment, new_comment=new_comment, session=session)
