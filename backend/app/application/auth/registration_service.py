import hashlib
import os
import random
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.application.user import service as user_service
from app.infrastructure.persistence.models.email_verification_code import (
    EmailVerificationCode,
)
from app.infrastructure.persistence.repositories.user_repository import (
    get_user_by_email,
)
from app.presentation.schemas.auth_schema import (
    RegisterUserRequest,
    SendVerificationCodeRequest,
    VerifyEmailCodeRequest,
)
from app.presentation.schemas.user.user_create import UserCreateSchema


def _hash_code(code: str) -> str:
    return hashlib.sha256(code.encode("utf-8")).hexdigest()


def _generate_code() -> str:
    return f"{random.randint(0, 99999):05d}"


def send_verification_code(db: Session, payload: SendVerificationCodeRequest) -> dict:
    if get_user_by_email(db, payload.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-mail já cadastrado.",
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
        expires_at=now + timedelta(minutes=15),
        verified=False,
    )
    db.add(record)
    db.commit()

    response: dict = {
        "message": "Código de verificação enviado.",
        "expires_in_minutes": 15,
    }
    if os.getenv("ENV", "development") != "production":
        response["verification_code"] = raw_code
    return response


def verify_email_code(db: Session, payload: VerifyEmailCodeRequest) -> dict:
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
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Código inválido.",
        )

    expiry = record.expires_at
    if expiry.tzinfo is None:
        expiry = expiry.replace(tzinfo=timezone.utc)
    if expiry < now:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Código expirado.",
        )

    record.verified = True
    record.expires_at = now + timedelta(hours=2)
    db.commit()
    return {"message": "E-mail verificado com sucesso.", "verified": True}


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
            detail="E-mail não verificado. Confirme o código antes de concluir o cadastro.",
        )

    from app.application.address.service import AddressService

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
