from datetime import datetime, timezone

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Index, Integer, String

from app.shared.infrastructure.database.connection import Base


class PhoneVerificationCode(Base):
    __tablename__ = "phone_verification_codes"
    __table_args__ = (
        CheckConstraint(
            "attempt_count >= 0",
            name="ck_phone_verification_codes_attempt_count_nonnegative",
        ),
        Index(
            "ix_phone_verification_codes_phone_created_at",
            "phone",
            "created_at",
        ),
    )

    id = Column(Integer, primary_key=True)
    phone = Column(String(20), nullable=False)
    code_hash = Column(String(255), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    verified = Column(Boolean, nullable=False, default=False)
    attempt_count = Column(Integer, nullable=False, default=0)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    def is_expired(self, at: datetime | None = None) -> bool:
        reference = at or datetime.now(timezone.utc)
        expires_at = self.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        return expires_at <= reference
