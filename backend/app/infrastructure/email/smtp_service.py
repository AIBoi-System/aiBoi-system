import logging
import os
import smtplib
from email.message import EmailMessage

logger = logging.getLogger(__name__)


class SmtpEmailService:
    """Sends transactional email via SMTP (TLS)."""

    def __init__(self) -> None:
        self._host = os.getenv("SMTP_HOST", "")
        self._port = int(os.getenv("SMTP_PORT", "587"))
        self._user = os.getenv("SMTP_USER", "")
        self._password = os.getenv("SMTP_PASSWORD", "")
        self._from_email = os.getenv("SMTP_FROM_EMAIL", self._user)
        self._use_tls = os.getenv("SMTP_USE_TLS", "true").lower() == "true"

    @property
    def is_configured(self) -> bool:
        return bool(self._host and self._from_email)

    def send_verification_code(self, to_email: str, code: str) -> None:
        subject = "AiBoi — Email verification code"
        body = (
            f"Your AiBoi verification code is: {code}\n\n"
            "This code expires in 15 minutes. "
            "If you did not request this, ignore this message."
        )
        self._send(to_email, subject, body)

    def _send(self, to_email: str, subject: str, body: str) -> None:
        env = os.getenv("ENV", "development")
        if not self.is_configured:
            if env == "production":
                raise RuntimeError("SMTP is not configured for production")
            logger.warning("SMTP not configured; email to %s was not sent", to_email)
            return

        message = EmailMessage()
        message["Subject"] = subject
        message["From"] = self._from_email
        message["To"] = to_email
        message.set_content(body)

        try:
            with smtplib.SMTP(self._host, self._port, timeout=30) as server:
                if self._use_tls:
                    server.starttls()
                if self._user and self._password:
                    server.login(self._user, self._password)
                server.send_message(message)
        except smtplib.SMTPException as exc:
            logger.exception("Failed to send email to %s", to_email)
            raise RuntimeError("Unable to send verification email") from exc









































