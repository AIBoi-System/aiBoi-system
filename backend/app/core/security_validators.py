"""Input validation helpers (OWASP-oriented, injection-safe text rules)."""

import re
from typing import Final

# Characters often used in XSS / SQL injection payloads in free-text fields.
_FORBIDDEN_SUBSTRINGS: Final[tuple[str, ...]] = (
    "<",
    ">",
    ";",
    "--",
    "/*",
    "*/",
    "xp_",
    "union ",
    "select ",
    "drop ",
    "insert ",
    "delete ",
    "update ",
)

_EMAIL_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$"
)


def normalize_email(email: str) -> str:
    """Normalize and validate email format before persistence."""
    normalized = email.strip().lower()
    if not _EMAIL_PATTERN.match(normalized):
        raise ValueError("Invalid email format")
    if len(normalized) > 255:
        raise ValueError("Email is too long")
    return normalized


def validate_safe_text(value: str, field_name: str, max_len: int = 150) -> str:
    """Reject dangerous patterns in user-controlled text (defense in depth)."""
    cleaned = value.strip()
    if not cleaned or len(cleaned) > max_len:
        raise ValueError(f"{field_name} is invalid")
    lowered = cleaned.lower()
    for token in _FORBIDDEN_SUBSTRINGS:
        if token in lowered:
            raise ValueError(f"{field_name} contains forbidden characters")
    return cleaned


def validate_password_strength(password: str) -> str:
    """Enforce password policy aligned with OWASP recommendations."""
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters")
    if len(password) > 128:
        raise ValueError("Password is too long")
    if not re.search(r"\d", password):
        raise ValueError("Password must include at least one number")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=\[\]\\;/]", password):
        raise ValueError("Password must include at least one symbol")
    if password.strip() != password:
        raise ValueError("Password must not start or end with whitespace")
    return password


def validate_zip_code(zip_code: str) -> str:
    digits = "".join(filter(str.isdigit, zip_code))
    if len(digits) != 8:
        raise ValueError("ZIP code must have 8 digits")
    return digits


def validate_state_uf(state: str) -> str:
    uf = state.strip().upper()
    if len(uf) != 2 or not uf.isalpha():
        raise ValueError("State must be a 2-letter UF code")
    return uf









































