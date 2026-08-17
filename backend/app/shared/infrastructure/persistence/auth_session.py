from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Index,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.shared.infrastructure.database.connection import Base


class AuthSession(Base):
    __tablename__ = "auth_sessions"
    __table_args__ = (
        CheckConstraint(
            "expires_at > created_at",
            name="ck_auth_sessions_expiry_after_creation",
        ),
        UniqueConstraint(
            "refresh_token_hash",
            name="uq_auth_sessions_refresh_token_hash",
        ),
        Index(
            "ix_auth_sessions_user_active",
            "user_id",
            "revoked_at",
            "expires_at",
        ),
        Index("ix_auth_sessions_expires_at", "expires_at"),
    )

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(
        ForeignKey(
            "users.id_user",
            name="fk_auth_sessions_user_id_users",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    refresh_token_hash = Column(String(64), nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    expires_at = Column(DateTime(timezone=True), nullable=False)
    last_used_at = Column(DateTime(timezone=True), nullable=True)
    revoked_at = Column(DateTime(timezone=True), nullable=True)
    replaced_by_session_id = Column(
        String(36),
        ForeignKey(
            "auth_sessions.id",
            name="fk_auth_sessions_replaced_by_session_id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )
    revocation_reason = Column(String(50), nullable=True)

    user = relationship("User", back_populates="auth_sessions")
    replacement = relationship(
        "AuthSession",
        remote_side=[id],
        foreign_keys=[replaced_by_session_id],
        post_update=True,
    )

    def is_active(self, at: datetime | None = None) -> bool:
        reference = at or datetime.now(timezone.utc)
        expires_at = self.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        return self.revoked_at is None and expires_at > reference

    def revoke(self, *, reason: str | None = None, at: datetime | None = None) -> None:
        self.revoked_at = at or datetime.now(timezone.utc)
        self.revocation_reason = reason
