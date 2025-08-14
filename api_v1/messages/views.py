from fastapi import APIRouter, status, Depends, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.messages.crud import send_message
from api_v1.messages.schemas import MessageRead, MessageCreate
from core.models import Message
from utils.db_helper import db_helper
from utils.token_helpers import get_user_by_token

router = APIRouter(prefix="/messages", tags=["Messages"])


@router.post("/message/{sent_to}", response_model=MessageRead, status_code=status.HTTP_200_OK)
async def send_message_view(request: Request, response: Response,
                            sent_to: int, message: MessageCreate,
                            session: AsyncSession = Depends(db_helper.session_getter)) -> Message:
    user = await get_user_by_token(request=request, response=response, session=session)
    return await send_message(sent_from=user.id, sent_to=sent_to, session=session, message=message)