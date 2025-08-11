import smtplib
import uuid
from email.message import EmailMessage

from core.config import settings


def send_email(recipient: str, subject: str, body: str):
    admin_email = settings.mail_config.admin_email
    message = EmailMessage()
    message["From"] = admin_email
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    with smtplib.SMTP(
        host=settings.mail_config.hostname, port=settings.mail_config.port
    ) as server:
        server.send_message(message)


def send_welcome_email(username: str, email: str):
    return send_email(recipient=email,
                      subject="Welcome to our site!",
                      body=f"Welcome to our site, {username}!")


def send_verification_email(user_id: int, user_email: str, verification_token: uuid.UUID):
    return send_email(recipient=user_email,
                      subject="Email verification",
                      body=f"Your verification code is {verification_token}. If this e-mail was sent by mistake just ignore it. The code is only valid for 60 minutes.")


def send_password_reset_token_email(user_email: str, password_reset_token: uuid.UUID):
    return send_email(recipient=user_email,
                      subject="Password reset",
                      body=f"Your password reset code is {password_reset_token}. This code is only valid for 60 minutes.")