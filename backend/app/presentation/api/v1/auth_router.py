import hashlib
import secrets
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.infrastructure.auth import create_access_token
from app.infrastructure.database.connection import get_db
from app.infrastructure.persistence.models.password_reset_token import PasswordResetToken
from app.infrastructure.persistence.repositories.user_repository import get_user_by_email
from app.infrastructure.security import hash_password, verify_password
from app.application.auth.registration_service import (
    register_user_with_address,
    send_verification_code,
    verify_email_code,
)
from app.presentation.schemas.auth_schema import (
    LoginRequest,
    PasswordResetConfirm,
    PasswordResetRequest,
    RegisterUserRequest,
    SendVerificationCodeRequest,
    TokenResponse,
    VerifyEmailCodeRequest,
)
from app.core.rate_limit import clear_attempts, is_rate_limited, record_attempt
from app.presentation.api.auth_dependencies import get_current_user
from app.presentation.schemas.user.user_response import UserResponseSchema

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup/send-code")
def signup_send_code(payload: SendVerificationCodeRequest, db: Session = Depends(get_db)):
    return send_verification_code(db, payload)


@router.post("/signup/verify-code")
def signup_verify_code(payload: VerifyEmailCodeRequest, db: Session = Depends(get_db)):
    return verify_email_code(db, payload)


@router.post("/signup/register", status_code=status.HTTP_201_CREATED)
def signup_register(payload: RegisterUserRequest, db: Session = Depends(get_db)):
    result = register_user_with_address(db, payload)
    user = result["user"]
    return {
        "message": "User registered successfully.",
        "user_id": user.id_user,
        "address_id": result["address_id"],
    }


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    rate_key = f"login:{payload.email}"
    if is_rate_limited(rate_key):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many login attempts. Please try again later.",
        )

    user = get_user_by_email(db, payload.email)
    if not user or not verify_password(payload.password, user.password):
        record_attempt(rate_key)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials.",
        )

    clear_attempts(rate_key)
    role = user.type or "user"
    token = create_access_token(subject=user.email, role=role)
    return TokenResponse(access_token=token, role=role)


@router.get("/me", response_model=UserResponseSchema)
def me(current_user=Depends(get_current_user)):
    return current_user


@router.post("/forgot-password")
def forgot_password(payload: PasswordResetRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, payload.email)
    if not user:
        return {"message": "If the account exists, a reset token has been generated."}

    raw_token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(raw_token.encode("utf-8")).hexdigest()
    reset = PasswordResetToken(
        user_id=user.id_user,
        token_hash=token_hash,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=30),
        used=False,
    )
    db.add(reset)
    db.commit()
    return {
        "message": "Reset token generated.",
        "reset_token": raw_token,
        "expires_in_minutes": 30,
    }


@router.post("/reset-password")
def reset_password(payload: PasswordResetConfirm, db: Session = Depends(get_db)):
    token_hash = hashlib.sha256(payload.token.encode("utf-8")).hexdigest()
    reset_record = (
        db.query(PasswordResetToken)
        .filter(
            PasswordResetToken.token_hash == token_hash,
            PasswordResetToken.used.is_(False),
        )
        .first()
    )
    if not reset_record:
        raise HTTPException(status_code=400, detail="Invalid reset token.")
    expiry = reset_record.expires_at
    if expiry.tzinfo is None:
        expiry = expiry.replace(tzinfo=timezone.utc)
    if expiry < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Reset token expired.")

    user = reset_record.user
    user.password = hash_password(payload.new_password)
    reset_record.used = True
    db.commit()
    return {"message": "Password updated successfully."}
