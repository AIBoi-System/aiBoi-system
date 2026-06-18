import hashlib
import os
import secrets
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

import app.shared.application.user.user_service as user_service
from app.core.rate_limit import clear_attempts, is_rate_limited, record_attempt
from app.infrastructure.email.smtp_service import SmtpEmailService
from app.shared.infrastructure.persistence.email_verification_code import (
    EmailVerificationCode,
)
from app.shared.infrastructure.persistence.user_repository import (
    get_user_by_email,
)
from app.presentation.schemas.auth_schema import (
    RegisterUserRequest,
    SendVerificationCodeRequest,
    VerifyEmailCodeRequest,
)
from app.presentation.schemas.user.user_create import UserCreateSchema

_CODE_TTL_MINUTES = 15
_VERIFIED_WINDOW_HOURS = 2
_email_service = SmtpEmailService()


def _hash_code(code: str) -> str:
    return hashlib.sha256(code.encode("utf-8")).hexdigest()


def _generate_code() -> str:
    return "".join(str(secrets.randbelow(10)) for _ in range(5))


def send_verification_code(db: Session, payload: SendVerificationCodeRequest) -> dict:
    rate_key = f"signup:send:{payload.email}"
    if is_rate_limited(rate_key, max_attempts=5):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many verification requests. Try again later.",
        )

    if get_user_by_email(db, payload.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered.",
        )

    raw_code = _generate_code()
    code_hash = _hash_code(raw_code)
    now = datetime.now(timezone.utc)

    db.query(EmailVerificationCode).filter(
        EmailVerificationCode.email == payload.email,
        EmailVerificationCode.verified.is_(False),
    ).delete(synchronize_session=False)

    record = EmailVerificationCode(
        email=payload.email,
        code_hash=code_hash,
        expires_at=now + timedelta(minutes=_CODE_TTL_MINUTES),
        verified=False,
    )
    db.add(record)
    db.commit()

    try:
        _email_service.send_verification_code(payload.email, raw_code)
    except RuntimeError:
        db.query(EmailVerificationCode).filter(
            EmailVerificationCode.id == record.id
        ).delete(synchronize_session=False)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to send verification email. Try again later.",
        ) from None

    record_attempt(rate_key)

    response: dict = {
        "message": "Verification code sent.",
        "expires_in_minutes": _CODE_TTL_MINUTES,
    }
    if os.getenv("ENV", "development") != "production":
        response["verification_code"] = raw_code
    return response


def verify_email_code(db: Session, payload: VerifyEmailCodeRequest) -> dict:
    rate_key = f"signup:verify:{payload.email}"
    if is_rate_limited(rate_key, max_attempts=10):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many verification attempts. Try again later.",
        )

    code_hash = _hash_code(payload.code)
    now = datetime.now(timezone.utc)

    record = (
        db.query(EmailVerificationCode)
        .filter(
            EmailVerificationCode.email == payload.email,
            EmailVerificationCode.code_hash == code_hash,
            EmailVerificationCode.verified.is_(False),
        )
        .order_by(EmailVerificationCode.created_at.desc())
        .first()
    )
    if not record:
        record_attempt(rate_key)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid verification code.",
        )

    expiry = record.expires_at
    if expiry.tzinfo is None:
        expiry = expiry.replace(tzinfo=timezone.utc)
    if expiry < now:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verification code expired.",
        )

    record.verified = True
    record.expires_at = now + timedelta(hours=_VERIFIED_WINDOW_HOURS)
    db.commit()
    clear_attempts(rate_key)
    return {"message": "Email verified successfully.", "verified": True}


def _email_is_verified(db: Session, email: str) -> bool:
    now = datetime.now(timezone.utc)
    record = (
        db.query(EmailVerificationCode)
        .filter(
            EmailVerificationCode.email == email,
            EmailVerificationCode.verified.is_(True),
        )
        .order_by(EmailVerificationCode.created_at.desc())
        .first()
    )
    if not record:
        return False
    expiry = record.expires_at
    if expiry.tzinfo is None:
        expiry = expiry.replace(tzinfo=timezone.utc)
    return expiry >= now


def register_user_with_address(db: Session, payload: RegisterUserRequest) -> dict:
    if not _email_is_verified(db, payload.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email not verified. Confirm the code before completing registration.",
        )

    from app.shared.application.address.address_service import AddressService

    address = AddressService.create_address(db, payload.address)
    user_data = UserCreateSchema(
        name=payload.name,
        email=payload.email,
        password=payload.password,
        cpf=payload.cpf,
        phone=payload.phone,
        address_id=address.id_address,
    )
    user = user_service.create_user_service(db, user_data)
    return {"user": user, "address_id": address.id_address}













