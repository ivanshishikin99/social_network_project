import uuid

from logger import log
from tasks.celery_conf import celery

from mailing.email_senders import send_welcome_email as send_welcome
from mailing.email_senders import send_verification_email as send_verification

@celery.task(bind=True, max_retries=5)
def send_welcome_email(self, user_id: int, username: str, email: str):
    try:
        log.info("Sending email to user with id: %s", user_id)
        return send_welcome(username=username, email=email)
    except:
        self.retry()


@celery.task(bind=True, max_retries=5)
def send_verification_email(self, user_id: int, user_email: str, verification_code: uuid.UUID):
    try:
        log.info("Sending verification email to user with id: %s", user_id)
        return send_verification(user_id=user_id, user_email=user_email, verification_token=verification_code)
    except:
        self.retry()