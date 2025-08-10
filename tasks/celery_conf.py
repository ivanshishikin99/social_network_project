from celery import Celery

from core.config import settings

celery = Celery(
    "tasks.celery",
    broker=f"{settings.celery_config.backend}://{settings.celery_config.hostname}:{settings.celery_config.port}//",
    backend="redis://",
)

celery.conf.update(
    result_backend=settings.celery_config.result_backend,
    broker_transport_options={
        "visibility_timeout": settings.celery_config.visibility_timeout
    },
    task_serializer=settings.celery_config.task_serializer,
    timezone=settings.celery_config.timezone,
)