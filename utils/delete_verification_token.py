import asyncio
import logging
from datetime import datetime, timedelta

from sqlalchemy import select

from core.config import settings
from core.models import VerificationToken
from utils.db_helper import db_helper


async def clean_verification_token_table(interval: int = 3600):
    logging.basicConfig(format=settings.log_config.log_format,
                        level=settings.log_config.log_level)
    log = logging.getLogger()
    while True:
        async with db_helper.session_maker() as session:
            statement = select(VerificationToken).where(datetime.now() - VerificationToken.created_at >= timedelta(hours=1))
            tokens = await session.execute(statement)
            tokens = tokens.scalars().all()
            for i in tokens:
                await session.delete(i)
                await session.commit()
            log.info("Verification table has been cleaned.")
        await asyncio.sleep(delay=interval)