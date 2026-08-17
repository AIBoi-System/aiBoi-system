from __future__ import annotations

import logging
import os
from typing import Protocol

logger = logging.getLogger(__name__)


class PhoneSender(Protocol):
    """Port for delivering short-lived phone verification codes."""

    def send_verification_code(self, phone: str, code: str) -> None: ...


class LocalPhoneSender:
    """Safe local placeholder until an SMS provider is explicitly selected.

    It never logs or persists the code. Production fails closed so a successful
    API response can never imply delivery when no provider exists.
    """

    def send_verification_code(self, phone: str, code: str) -> None:
        del code
        if os.getenv("ENV", "development").casefold() == "production":
            raise RuntimeError("Phone verification provider is not configured")
        masked = f"***{phone[-4:]}" if len(phone) >= 4 else "***"
        logger.info(
            "Local phone verification requested for %s; no external message was sent",
            masked,
        )
