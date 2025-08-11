import uuid

from logger import log
from tasks.celery_conf import celery

from mailing.email_senders import send_welcome_email as send_welcome
from mailing.email_senders import send_verification_email as send_verification
from mailing.email_senders import send_password_reset_token_email as send_reset

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

@celery.task(bind=True, max_retries=5)
def send_password_reset_email(self, user_email: str, password_reset_token: uuid.UUID):
    try:
        log.info("Sending password reset email %s", user_email)
        return send_reset(user_email=user_email, password_reset_token=password_reset_token)
    except:
        self.retry()