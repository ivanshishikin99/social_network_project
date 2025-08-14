from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.messages.schemas import MessageCreate
from core.models import Message


async def send_message(sent_from: int, sent_to: int, message: MessageCreate, session: AsyncSession) -> Message:
    message = Message(**message.model_dump())
    message.sent_from = sent_from
    message.sent_to = sent_to
    session.add(message)
    await session.commit()
    return message
