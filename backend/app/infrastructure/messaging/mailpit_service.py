from __future__ import annotations

import os
import smtplib
from email.message import EmailMessage


class MailpitDeliveryService:
    """Deliver development email and simulated SMS into a local Mailpit inbox."""

    _LOOPBACK_HOSTS = frozenset({"127.0.0.1", "localhost", "::1", "mailpit", "host.docker.internal"})

    def __init__(self) -> None:
        environment = os.getenv("ENV", "development").strip().casefold()
        if environment == "production":
            raise RuntimeError("Mailpit delivery is forbidden in production")

        self._host = os.getenv("MAILPIT_SMTP_HOST", "127.0.0.1").strip()
        if self._host.casefold() not in self._LOOPBACK_HOSTS:
            raise RuntimeError("Mailpit must be bound to a loopback host")

        self._port = int(os.getenv("MAILPIT_SMTP_PORT", "1025"))
        if not 1 <= self._port <= 65535:
            raise RuntimeError("Invalid Mailpit SMTP port")

        self._from_email = os.getenv(
            "MAILPIT_FROM_EMAIL",
            "no-reply@agrofence.local",
        ).strip()

    def send_verification_code(self, to_email: str, code: str) -> None:
        self._send(
            recipient=to_email,
            subject="[AgroFence local] Confirmação de e-mail",
            body=(
                f"Seu código de confirmação de e-mail é: {code}\n\n"
                "Ele expira em 15 minutos. Esta mensagem foi capturada "
                "localmente pelo Mailpit e não saiu deste computador."
            ),
            delivery_type="email",
        )

    def send_password_reset(self, to_email: str, raw_token: str) -> None:
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
        self._send(
            recipient=to_email,
            subject="[AgroFence local] Redefinição de senha",
            body=(
                "Use o link local para redefinir sua senha:\n\n"
                f"{frontend_url}/reset-password?token={raw_token}\n\n"
                "O token expira em 30 minutos e esta mensagem não saiu "
                "deste computador."
            ),
            delivery_type="password-reset",
        )

    def send_phone_verification_code(self, phone: str, code: str) -> None:
        last_four = phone[-4:] if len(phone) >= 4 else "local"
        self._send(
            recipient=f"sms-{last_four}@agrofence.local",
            subject=f"[AgroFence local] SMS simulado para ***{last_four}",
            body=(
                f"Seu código de confirmação do celular é: {code}\n\n"
                "Este é um SMS simulado para desenvolvimento. Ele não "
                "comprova a posse de um número real."
            ),
            delivery_type="simulated-sms",
        )

    def _send(
        self,
        *,
        recipient: str,
        subject: str,
        body: str,
        delivery_type: str,
    ) -> None:
        message = EmailMessage()
        message["Subject"] = subject
        message["From"] = self._from_email
        message["To"] = recipient
        message["X-AgroFence-Delivery"] = delivery_type
        message.set_content(body)

        try:
            with smtplib.SMTP(self._host, self._port, timeout=5) as server:
                server.send_message(message)
        except (OSError, smtplib.SMTPException) as exc:
            raise RuntimeError("Local Mailpit delivery is unavailable") from exc


class MailpitPhoneSender:
    """Phone port adapter that represents a local SMS inside Mailpit."""

    def __init__(self, delivery: MailpitDeliveryService) -> None:
        self._delivery = delivery

    def send_verification_code(self, phone: str, code: str) -> None:
        self._delivery.send_phone_verification_code(phone, code)
