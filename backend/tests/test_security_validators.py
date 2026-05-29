import pytest

from app.core.security_validators import (
    normalize_email,
    validate_password_strength,
    validate_safe_text,
    validate_zip_code,
)


def test_normalize_email_valid():
    assert normalize_email("  User@Example.COM ") == "user@example.com"


def test_normalize_email_invalid():
    with pytest.raises(ValueError):
        normalize_email("not-an-email")


def test_validate_safe_text_blocks_sql_injection():
    with pytest.raises(ValueError):
        validate_safe_text("'; DROP TABLE users; --", "name")


def test_validate_password_strength():
    validate_password_strength("Abcdef1!")
    with pytest.raises(ValueError):
        validate_password_strength("short")


def test_validate_zip_code():
    assert validate_zip_code("12345-678") == "12345678"
