"""AiBoi API — Application entry point.

Security & Configuration
------------------------
* CORS: explicitly configured per environment; wildcard (*) forbidden in production.
* Rate limiting: Redis-backed when REDIS_URL is set; in-memory fallback for dev.
* JWT: validated at import time (auth.py raises RuntimeError in prod if key is missing).
* Security headers: added via middleware for all responses.
"""

from __future__ import annotations

import logging
import os

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.shared.infrastructure.database.connection import get_db
from app.infrastructure.persistence import models  # noqa: F401 — registra tabelas
from app.presentation.api.exception_handlers import register_exception_handlers
from app.presentation.api.v1.router import api_v1_router

logger = logging.getLogger(__name__)

_ENV: str = os.getenv("ENV", "development").lower()
_IS_PRODUCTION: bool = _ENV == "production"


# ---------------------------------------------------------------------------
# CORS configuration
# ---------------------------------------------------------------------------


def _resolve_cors_origins() -> list[str]:
    """Resolve and validate CORS allowed origins.

    Production rules:
    * CORS_ALLOWED_ORIGINS must be explicitly set.
    * Wildcard (*) is not allowed (violates same-origin security policy).

    Development fallback: allows common local dev ports.
    """
    raw = os.getenv("CORS_ALLOWED_ORIGINS", "")

    if not raw or raw.strip() == "*":
        if _IS_PRODUCTION:
            raise RuntimeError(
                "FATAL: CORS_ALLOWED_ORIGINS must be explicitly set in production. "
                "Wildcard (*) is not permitted. "
                "Example: CORS_ALLOWED_ORIGINS=https://app.aiboi.com.br"
            )
        logger.warning(
            "CORS_ALLOWED_ORIGINS not set — using empty origins. "
            "Set CORS_ALLOWED_ORIGINS to allow requests."
        )
        return []

    origins = [o.strip() for o in raw.split(",") if o.strip()]

    if _IS_PRODUCTION and "*" in origins:
        raise RuntimeError(
            "FATAL: Wildcard (*) is not allowed in CORS_ALLOWED_ORIGINS in production. "
            "Specify explicit origins."
        )

    return origins


allowed_origins = _resolve_cors_origins()

# ---------------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------------

app = FastAPI(
    title="AiBoi API",
    version="2.0.0",
    description="Gestão bovina — Clean Architecture + DDD",
)

register_exception_handlers(app)
app.include_router(api_v1_router, prefix="/api/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Startup validation
# ---------------------------------------------------------------------------


@app.on_event("startup")
async def validate_startup_config() -> None:
    """Validate critical configuration at startup and fail fast if misconfigured."""
    logger.info("AiBoi API starting — env=%s, CORS origins=%s", _ENV, allowed_origins)

    # Validate Redis availability when configured
    redis_url = os.getenv("REDIS_URL")
    if _IS_PRODUCTION and not redis_url:
        raise RuntimeError(
            "REDIS_URL is required in production for distributed rate limiting."
        )
    if redis_url:
        try:
            import redis as redis_lib  # type: ignore[import]

            r = redis_lib.from_url(redis_url, socket_connect_timeout=3)
            r.ping()
            logger.info("Redis connected — distributed rate limiting is active.")
        except Exception as exc:
            if _IS_PRODUCTION:
                raise RuntimeError(
                    "Redis is required and must be reachable in production for "
                    "distributed rate limiting."
                ) from exc
            else:
                logger.warning(
                    "Redis unavailable (%s) — falling back to in-memory rate limiting.", exc
                )
    else:
        logger.warning(
            "REDIS_URL not set — using in-memory rate limiting. "
            "NOT safe for multi-instance deployments."
        )


# ---------------------------------------------------------------------------
# Security headers middleware
# ---------------------------------------------------------------------------


@app.middleware("http")
async def security_headers_middleware(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    if request.url.path.startswith("/docs") or request.url.path.startswith("/redoc"):
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "img-src 'self' data: https://fastapi.tiangolo.com"
        )
    else:
        response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response


# ---------------------------------------------------------------------------
# Health / diagnostic endpoints
# ---------------------------------------------------------------------------


@app.get("/", tags=["Health"])
def read_root():
    return {"status": "Online", "projeto": "AiBoi", "arquitetura": "Clean + DDD"}


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}


@app.get("/test-db", tags=["Health"])
def test_db_connection(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {
            "status": "sucesso",
            "message": "Conexão com banco OK",
        }
    except Exception:
        return {"status": "erro", "message": "Falha na conexão com o banco"}
