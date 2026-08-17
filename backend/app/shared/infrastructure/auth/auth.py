"""JWT token creation and validation.

Security rules
--------------
* In **production** (ENV=production) the JWT_SECRET_KEY must be explicitly set in the
  environment and must be at least 32 characters.  The application will refuse to start
  if this condition is not met, preventing the silent fallback to a random key that
  would invalidate all existing tokens on every restart.

* In **development / test** a deterministic insecure key is used and a warning is
  emitted.  The random-key fallback that was present before this fix is intentionally
  removed because it caused hard-to-debug 401 errors after any server restart.
"""

from __future__ import annotations

import logging
import os
import warnings
from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import uuid4

from jose import ExpiredSignatureError, JWTError, jwt
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

_ENV: str = os.getenv("ENV", "development").lower()
_IS_PRODUCTION: bool = _ENV == "production"

_RAW_SECRET: str | None = os.getenv("JWT_SECRET_KEY")

# Minimum acceptable length for the secret key (OWASP recommends ≥ 256-bit = 32 bytes)
_MIN_SECRET_LEN: int = 32

_DEV_FALLBACK_KEY: str = "dev-only-insecure-key-do-not-use-in-production-aiboi"


def _resolve_secret_key() -> str:
    """Validate and return the JWT secret key.

    Raises
    ------
    RuntimeError
        In production if the key is missing or too short.
    """
    raw = _RAW_SECRET

    if not raw or raw in ("your-secret-key", "change-me-to-a-long-random-secret"):
        if _IS_PRODUCTION:
            raise RuntimeError(
                "FATAL: JWT_SECRET_KEY is not set (or uses the placeholder value). "
                "Set a strong, random secret of at least 32 characters in your "
                "production environment variables before starting the server."
            )
        warnings.warn(
            "JWT_SECRET_KEY is not configured — using an insecure development key. "
            "All tokens will be invalid across environments and after server restarts. "
            "Set JWT_SECRET_KEY in your .env file for local development.",
            stacklevel=2,
        )
        return _DEV_FALLBACK_KEY

    if len(raw) < _MIN_SECRET_LEN:
        if _IS_PRODUCTION:
            raise RuntimeError(
                f"FATAL: JWT_SECRET_KEY is too short ({len(raw)} chars). "
                f"It must be at least {_MIN_SECRET_LEN} characters in production."
            )
        warnings.warn(
            f"JWT_SECRET_KEY is only {len(raw)} chars (minimum recommended: {_MIN_SECRET_LEN}). "
            "Consider using a longer secret for better security.",
            stacklevel=2,
        )

    return raw


SECRET_KEY: str = _resolve_secret_key()
ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))
REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("JWT_REFRESH_EXPIRE_DAYS", "7"))

# Log key configuration (never log the key itself)
logger.info(
    "JWT configured — algorithm=%s, access_ttl=%dm, refresh_ttl=%dd, env=%s",
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
    _ENV,
)

# ---------------------------------------------------------------------------
# Token creation
# ---------------------------------------------------------------------------


def create_access_token(
    subject: str,
    role: str,
    expires_delta: Optional[timedelta] = None,
    session_id: str | None = None,
) -> str:
    """Create a signed JWT access token."""
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    payload = {
        "exp": expire,
        "sub": str(subject),
        "role": role,
        "type": "access",
        "jti": str(uuid4()),
    }
    if session_id:
        payload["sid"] = session_id
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(
    subject: str,
    role: str,
    expires_delta: Optional[timedelta] = None,
    session_id: str | None = None,
) -> str:
    """Create a signed JWT refresh token (longer-lived, type=refresh).

    The refresh token should be stored securely by the client (e.g.
    HttpOnly cookie or encrypted storage) and used only to obtain a new
    access token via the /auth/refresh endpoint.
    """
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )
    payload = {
        "exp": expire,
        "sub": str(subject),
        "role": role,
        "type": "refresh",
        "jti": str(uuid4()),
    }
    if session_id:
        payload["sid"] = session_id
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


# ---------------------------------------------------------------------------
# Token validation
# ---------------------------------------------------------------------------


def decode_access_token(token: str) -> dict:
    """Decode and validate an access token.

    Raises
    ------
    ValueError
        If the token is expired or invalid.
    """
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if decoded.get("type") != "access":
            raise ValueError("Token is not a valid access token.")
        return decoded
    except ExpiredSignatureError:
        raise ValueError("Token has expired.")
    except JWTError:
        raise ValueError("Invalid token.")


def decode_refresh_token(token: str) -> dict:
    """Decode and validate a refresh token.

    Raises
    ------
    ValueError
        If the token is expired, invalid, or not a refresh token.
    """
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if decoded.get("type") != "refresh":
            raise ValueError("Token is not a valid refresh token.")
        return decoded
    except ExpiredSignatureError:
        raise ValueError("Refresh token has expired. Please log in again.")
    except JWTError:
        raise ValueError("Invalid refresh token.")
