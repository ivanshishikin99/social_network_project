from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.messages.crud import get_message_by_id
from core.models import Message
from utils.db_helper import db_helper


async def get_message_by_id_dependency(message_id: int, session: AsyncSession = Depends(db_helper)) -> Message | HTTPException:
    try:
        message = await get_message_by_id(message_id=message_id, session=session)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found!")
    return message