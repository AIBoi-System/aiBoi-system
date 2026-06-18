"""Simple in-memory rate limiting (per-process; use Redis in multi-instance production)."""

from datetime import datetime, timedelta, timezone
from typing import Final

_MAX_ATTEMPTS: Final[int] = 5
_WINDOW: Final[timedelta] = timedelta(minutes=5)

_buckets: dict[str, list[datetime]] = {}


def is_rate_limited(key: str, *, max_attempts: int = _MAX_ATTEMPTS) -> bool:
    now = datetime.now(timezone.utc)
    attempts = [ts for ts in _buckets.get(key, []) if now - ts < _WINDOW]
    _buckets[key] = attempts
    return len(attempts) >= max_attempts


def record_attempt(key: str) -> None:
    now = datetime.now(timezone.utc)
    attempts = _buckets.setdefault(key, [])
    attempts.append(now)
    _buckets[key] = [ts for ts in attempts if now - ts < _WINDOW]


def clear_attempts(key: str) -> None:
    _buckets.pop(key, None)









































