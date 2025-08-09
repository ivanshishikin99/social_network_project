import logging

from core.config import settings

logging.basicConfig(
    level=settings.log_config.log_level, format=settings.log_config.log_format
)

log = logging.getLogger(__name__)