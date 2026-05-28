"""Compatibilidade — use app.infrastructure.security."""

from app.infrastructure.security import hash_password, verify_password

__all__ = ["hash_password", "verify_password"]
