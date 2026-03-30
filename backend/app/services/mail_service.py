from __future__ import annotations

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.exceptions import AppError
from app.core.security import TokenService
from app.core.settings import Settings


class EmailVerificationService:
    def __init__(self, settings: Settings, token_service: TokenService) -> None:
        self._settings = settings
        self._token_service = token_service

    def send_verification_email(self, receiver_email: str, receiver_type: str) -> None:
        if not (
            self._settings.email_smtp_server
            and self._settings.email_smtp_user
            and self._settings.email_smtp_password
        ):
            raise AppError("邮件服务未配置", status_code=503)

        message = MIMEMultipart()
        message["From"] = self._settings.email_smtp_user
        message["To"] = receiver_email
        message["Subject"] = "新账号验证"

        token = self._token_service.create_token(
            {"email": receiver_email, "usertype": receiver_type}
        )
        verify_url = (
            f"{self._settings.public_base_url.rstrip('/')}/user/verify?token={token}"
        )
        content = f"请点击链接验证账号：{verify_url}"
        message.attach(MIMEText(content, "plain"))

        with smtplib.SMTP_SSL(
            self._settings.email_smtp_server, self._settings.email_smtp_port
        ) as server:
            server.ehlo()
            server.login(
                self._settings.email_smtp_user,
                self._settings.email_smtp_password,
            )
            server.sendmail(
                self._settings.email_smtp_user,
                receiver_email,
                message.as_string(),
            )
