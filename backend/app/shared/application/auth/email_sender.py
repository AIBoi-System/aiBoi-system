from typing import Protocol


class EmailSender(Protocol):
    """Port for transactional authentication messages."""

    def send_verification_code(self, to_email: str, code: str) -> None: ...

    def send_password_reset(self, to_email: str, raw_token: str) -> None: ...
