from typing import Sequence

from sqlalchemy import select
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


async def get_all_messages_for_user(user_id: int, session: AsyncSession) -> Sequence[Message]:
    statement = select(Message).where(Message.sent_to == user_id)
    messages = await session.execute(statement)
    messages = messages.scalars().all()
    return messages


async def get_message_by_id(message_id: int, session: AsyncSession) -> Message | None:
    return await session.get(Message, message_id)

