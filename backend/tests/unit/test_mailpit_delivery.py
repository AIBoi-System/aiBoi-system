from email.message import EmailMessage

import pytest

from app.infrastructure.messaging.mailpit_service import (
    MailpitDeliveryService,
    MailpitPhoneSender,
)
from app.presentation.api.auth_dependencies import _delivery_mode


class FakeSmtp:
    messages: list[EmailMessage] = []

    def __init__(self, host: str, port: int, timeout: int) -> None:
        assert host == "127.0.0.1"
        assert port == 1025
        assert timeout == 5

    def __enter__(self):
        return self

    def __exit__(self, *_args) -> None:
        return None

    def send_message(self, message: EmailMessage) -> None:
        self.messages.append(message)


@pytest.fixture(autouse=True)
def reset_fake_smtp(monkeypatch):
    FakeSmtp.messages = []
    monkeypatch.setenv("ENV", "development")
    monkeypatch.setattr(
        "app.infrastructure.messaging.mailpit_service.smtplib.SMTP",
        FakeSmtp,
    )


def test_mailpit_delivers_email_and_simulated_sms_without_exposing_full_phone():
    delivery = MailpitDeliveryService()

    delivery.send_verification_code("owner@example.com", "12345")
    MailpitPhoneSender(delivery).send_verification_code("11987654321", "54321")

    assert len(FakeSmtp.messages) == 2
    email_message, sms_message = FakeSmtp.messages
    assert email_message["To"] == "owner@example.com"
    assert "12345" in email_message.get_content()
    assert sms_message["To"] == "sms-4321@agrofence.local"
    assert "11987654321" not in sms_message.as_string()
    assert "54321" in sms_message.get_content()


def test_mailpit_is_forbidden_in_production(monkeypatch):
    monkeypatch.setenv("ENV", "production")

    with pytest.raises(RuntimeError, match="forbidden in production"):
        MailpitDeliveryService()


def test_mailpit_refuses_non_loopback_smtp(monkeypatch):
    monkeypatch.setenv("MAILPIT_SMTP_HOST", "mail.example.com")

    with pytest.raises(RuntimeError, match="loopback"):
        MailpitDeliveryService()


def test_delivery_mode_rejects_unknown_configuration(monkeypatch):
    monkeypatch.setenv("AUTH_DELIVERY_MODE", "typo")

    with pytest.raises(RuntimeError, match="mailpit or provider"):
        _delivery_mode()


def test_test_environment_never_uses_mailpit(monkeypatch):
    monkeypatch.setenv("ENV", "test")
    monkeypatch.setenv("AUTH_DELIVERY_MODE", "mailpit")

    assert _delivery_mode() == "provider"
