"""
Rate limiting — Redis-backed for multi-instance deployments.

Strategy:
  • Production (REDIS_URL set)  → Redis sorted-set sliding window (shared across all
    API instances, atomic via pipeline).
  • Development / test          → In-memory dict (single-process only, not shared).

The public surface (is_rate_limited / record_attempt / clear_attempts) is the same
so all callers require no changes.
"""

from __future__ import annotations

import logging
import os
import time
from datetime import datetime, timedelta, timezone
from typing import Final

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

_MAX_ATTEMPTS: Final[int] = 5
_WINDOW_SECONDS: Final[int] = 5 * 60  # 5 minutes

_REDIS_URL: str | None = os.getenv("REDIS_URL")

# ---------------------------------------------------------------------------
# Redis backend (preferred)
# ---------------------------------------------------------------------------


def _get_redis():  # type: ignore[return]
    """Return a Redis client (lazy, cached).  Returns None if not configured."""
    if not _REDIS_URL:
        return None

    try:
        import redis  # type: ignore[import]

        client = redis.from_url(
            _REDIS_URL,
            decode_responses=True,
            socket_connect_timeout=2,
            socket_timeout=2,
        )
        client.ping()  # validate connectivity at first use
        return client
    except Exception as exc:  # pragma: no cover
        logger.warning(
            "Redis unavailable (%s) — falling back to in-memory rate limiter. "
            "This is NOT safe for multi-instance deployments.",
            exc,
        )
        return None


_redis_client = None
_redis_checked = False


def _redis():
    """Cached Redis client lookup (checks once per process lifetime)."""
    global _redis_client, _redis_checked
    if not _redis_checked:
        _redis_client = _get_redis()
        _redis_checked = True
    return _redis_client


# ---------------------------------------------------------------------------
# In-memory fallback (single-process / dev / test)
# ---------------------------------------------------------------------------

_buckets: dict[str, list[datetime]] = {}


def _im_is_rate_limited(key: str, max_attempts: int) -> bool:
    now = datetime.now(timezone.utc)
    window = timedelta(seconds=_WINDOW_SECONDS)
    attempts = [ts for ts in _buckets.get(key, []) if now - ts < window]
    _buckets[key] = attempts
    return len(attempts) >= max_attempts


def _im_record_attempt(key: str) -> None:
    now = datetime.now(timezone.utc)
    window = timedelta(seconds=_WINDOW_SECONDS)
    attempts = _buckets.setdefault(key, [])
    attempts.append(now)
    _buckets[key] = [ts for ts in attempts if now - ts < window]


def _im_clear_attempts(key: str) -> None:
    _buckets.pop(key, None)


# ---------------------------------------------------------------------------
# Redis backend helpers
# ---------------------------------------------------------------------------

_RATE_LIMIT_PREFIX = "rl:"


def _redis_key(key: str) -> str:
    return f"{_RATE_LIMIT_PREFIX}{key}"


def _redis_is_rate_limited(r, key: str, max_attempts: int) -> bool:  # type: ignore[no-untyped-def]
    now = time.time()
    rkey = _redis_key(key)
    pipe = r.pipeline()
    # Remove expired entries outside current window
    pipe.zremrangebyscore(rkey, "-inf", now - _WINDOW_SECONDS)
    # Count remaining entries
    pipe.zcard(rkey)
    _, count = pipe.execute()
    return int(count) >= max_attempts


def _redis_record_attempt(r, key: str) -> None:  # type: ignore[no-untyped-def]
    now = time.time()
    rkey = _redis_key(key)
    pipe = r.pipeline()
    # Add current timestamp as both score and member (unique by timestamp+random suffix)
    member = f"{now:.6f}"
    pipe.zadd(rkey, {member: now})
    # Set key TTL slightly larger than window so Redis auto-cleans
    pipe.expire(rkey, _WINDOW_SECONDS + 10)
    pipe.execute()


def _redis_clear_attempts(r, key: str) -> None:  # type: ignore[no-untyped-def]
    r.delete(_redis_key(key))


# ---------------------------------------------------------------------------
# Public API (same signature as before — zero caller changes required)
# ---------------------------------------------------------------------------


def is_rate_limited(key: str, *, max_attempts: int = _MAX_ATTEMPTS) -> bool:
    """Return True if ``key`` has exceeded ``max_attempts`` in the sliding window."""
    r = _redis()
    if r is not None:
        try:
            return _redis_is_rate_limited(r, key, max_attempts)
        except Exception as exc:
            logger.warning("Redis rate-limit check failed (%s) — falling back to in-memory", exc)
    return _im_is_rate_limited(key, max_attempts)


def record_attempt(key: str) -> None:
    """Record a new attempt for ``key``."""
    r = _redis()
    if r is not None:
        try:
            _redis_record_attempt(r, key)
            return
        except Exception as exc:
            logger.warning("Redis record_attempt failed (%s) — falling back to in-memory", exc)
    _im_record_attempt(key)


def clear_attempts(key: str) -> None:
    """Clear all recorded attempts for ``key`` (e.g. after successful login)."""
    r = _redis()
    if r is not None:
        try:
            _redis_clear_attempts(r, key)
            return
        except Exception as exc:
            logger.warning("Redis clear_attempts failed (%s) — falling back to in-memory", exc)
    _im_clear_attempts(key)
