from __future__ import annotations

import hashlib
import secrets
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.rate_limit import clear_attempts, is_rate_limited, record_attempt
from app.presentation.schemas.auth_schema import RegisterUserRequest
from app.shared.application.auth.email_sender import EmailSender
from app.shared.application.auth.phone_sender import PhoneSender
from app.shared.domain.exceptions import ValidationException
from app.shared.domain.registration import Registration
from app.shared.domain.value_objects import BrazilianAddress
from app.shared.infrastructure.auth.auth import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
)
from app.shared.infrastructure.auth.security import hash_password, verify_password
from app.shared.infrastructure.persistence.auth_repository import AuthRepository
from app.shared.infrastructure.persistence.cpf import CPF as PersistentCPF
from app.shared.infrastructure.persistence.email_verification_code import EmailVerificationCode
from app.shared.infrastructure.persistence.password_reset_token import PasswordResetToken
from app.shared.infrastructure.persistence.phone_verification_code import PhoneVerificationCode

_CODE_TTL_MINUTES = 15
_VERIFIED_WINDOW_HOURS = 2
_PHONE_MAX_ATTEMPTS = 5


def _hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _generate_code() -> str:
    return "".join(str(secrets.randbelow(10)) for _ in range(5))


def _aware(value: datetime) -> datetime:
    return value if value.tzinfo else value.replace(tzinfo=timezone.utc)


def _rate_key(scope: str, destination: str) -> str:
    return f"{scope}:{_hash(destination.casefold())}"


def _unauthorized() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )


@dataclass(frozen=True)
class IssuedTokens:
    access_token: str
    refresh_token: str
    role: str


class AuthService:
    def __init__(
        self,
        db: Session,
        phone_sender: PhoneSender,
        email_sender: EmailSender,
    ) -> None:
        self.db = db
        self.repo = AuthRepository(db)
        self.phone_sender = phone_sender
        self.email_sender = email_sender

    def send_email_code(self, email: str) -> dict:
        key = _rate_key("signup:send-email", email)
        if is_rate_limited(key, max_attempts=5):
            raise HTTPException(status_code=429, detail="Too many verification requests.")
        # Same response for registered and unknown destinations.
        if self.repo.get_user_by_email(email):
            record_attempt(key)
            return self._sent_response()
        code = _generate_code()
        now = datetime.now(timezone.utc)
        record = EmailVerificationCode(
            email=email, code_hash=_hash(code),
            expires_at=now + timedelta(minutes=_CODE_TTL_MINUTES), verified=False,
        )
        self.repo.replace_pending_email_code(record)
        self.db.commit()
        try:
            self.email_sender.send_verification_code(email, code)
        except RuntimeError:
            self.db.delete(record)
            self.db.commit()
            raise HTTPException(status_code=503, detail="Unable to send verification message.") from None
        record_attempt(key)
        return self._sent_response()

    def send_phone_code(self, phone: str) -> dict:
        key = _rate_key("signup:send-phone", phone)
        if is_rate_limited(key, max_attempts=5):
            raise HTTPException(status_code=429, detail="Too many verification requests.")
        if self.repo.get_user_by_phone(phone):
            record_attempt(key)
            return self._sent_response()
        code = _generate_code()
        now = datetime.now(timezone.utc)
        record = PhoneVerificationCode(
            phone=phone, code_hash=_hash(code),
            expires_at=now + timedelta(minutes=_CODE_TTL_MINUTES),
            verified=False, attempt_count=0,
        )
        self.repo.replace_pending_phone_code(record)
        self.db.commit()
        try:
            self.phone_sender.send_verification_code(phone, code)
        except RuntimeError:
            self.db.delete(record)
            self.db.commit()
            raise HTTPException(status_code=503, detail="Unable to send verification message.") from None
        record_attempt(key)
        return self._sent_response()

    @staticmethod
    def _sent_response() -> dict:
        return {"message": "If eligible, a verification code has been sent.", "expires_in_minutes": _CODE_TTL_MINUTES}

    def verify_email_code(self, email: str, code: str) -> dict:
        key = _rate_key("signup:verify-email", email)
        if is_rate_limited(key, max_attempts=10):
            raise HTTPException(status_code=429, detail="Too many verification attempts.")
        record = self.repo.latest_email_code(email)
        now = datetime.now(timezone.utc)
        if not record or record.verified or _aware(record.expires_at) <= now or not secrets.compare_digest(record.code_hash, _hash(code)):
            record_attempt(key)
            self.db.rollback()
            raise HTTPException(status_code=400, detail="Invalid or expired verification code.")
        record.verified = True
        record.expires_at = now + timedelta(hours=_VERIFIED_WINDOW_HOURS)
        self.db.commit()
        clear_attempts(key)
        return {"message": "Email verified successfully.", "verified": True}

    def verify_phone_code(self, phone: str, code: str) -> dict:
        key = _rate_key("signup:verify-phone", phone)
        if is_rate_limited(key, max_attempts=_PHONE_MAX_ATTEMPTS):
            raise HTTPException(status_code=429, detail="Too many verification attempts.")
        record = self.repo.latest_phone_code(phone)
        now = datetime.now(timezone.utc)
        valid = bool(record and not record.verified and record.attempt_count < _PHONE_MAX_ATTEMPTS and _aware(record.expires_at) > now and secrets.compare_digest(record.code_hash, _hash(code)))
        if not valid:
            if record and not record.verified:
                record.attempt_count += 1
                self.db.commit()
            else:
                self.db.rollback()
            record_attempt(key)
            raise HTTPException(status_code=400, detail="Invalid or expired verification code.")
        record.verified = True
        record.expires_at = now + timedelta(hours=_VERIFIED_WINDOW_HOURS)
        self.db.commit()
        clear_attempts(key)
        return {"message": "Phone verified successfully.", "verified": True}

    def register(self, payload: RegisterUserRequest) -> tuple[object, int, IssuedTokens]:
        now = datetime.now(timezone.utc)
        email_record = self.repo.verified_email_code(str(payload.email), now)
        phone_record = self.repo.verified_phone_code(payload.phone, now)
        if not email_record or not phone_record:
            self.db.rollback()
            raise HTTPException(status_code=400, detail="Email and phone verification are required.")
        try:
            registration = Registration.start(email=str(payload.email), phone=payload.phone)
            registration.verify_email(str(payload.email))
            registration.verify_phone(payload.phone)
            address = BrazilianAddress(**payload.address.model_dump())
            registration.set_profile(name=payload.name, cpf=payload.cpf, address=address)
            registration.set_password_hash(hash_password(payload.password))
            completed = registration.complete()
            formatted_cpf = str(PersistentCPF(completed.cpf))
            if self.repo.get_user_by_email(completed.email) or self.repo.get_user_by_phone(completed.phone) or self.repo.get_user_by_cpf(formatted_cpf):
                raise HTTPException(status_code=409, detail="Registration data is already in use.")
            user, persisted_address = self.repo.create_user_with_address(
                name=completed.name, email=completed.email, phone=completed.phone,
                cpf=formatted_cpf, password_hash=completed.password_hash,
                address_data={
                    "zip_code": completed.address.zip_code, "state": completed.address.state,
                    "neighborhood": completed.address.neighborhood, "street_name": completed.address.street_name,
                    "number": completed.address.number, "complement": completed.address.complement,
                },
            )
            self.repo.consume_verifications(email_record, phone_record)
            tokens = self._issue_session(user)
            self.db.commit()
            return user, persisted_address.id_address, tokens
        except HTTPException:
            self.db.rollback()
            raise
        except (ValidationException, ValueError) as exc:
            self.db.rollback()
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        except IntegrityError as exc:
            self.db.rollback()
            raise HTTPException(
                status_code=409,
                detail="Registration data is already in use.",
            ) from exc
        except Exception:
            self.db.rollback()
            raise

    def login(self, email: str, password: str) -> IssuedTokens:
        key = _rate_key("login", email)
        if is_rate_limited(key):
            raise HTTPException(status_code=429, detail="Too many login attempts.")
        user = self.repo.get_user_by_email(email)
        active = user and str(user.account_status or "").casefold() in {"ativo", "active"}
        if not active or not verify_password(password, user.password):
            record_attempt(key)
            raise HTTPException(status_code=401, detail="Invalid credentials.")
        tokens = self._issue_session(user)
        self.db.commit()
        clear_attempts(key)
        return tokens

    def _issue_session(self, user) -> IssuedTokens:
        session_id = str(uuid4())
        role = user.type or "user"
        refresh = create_refresh_token(subject=user.email, role=role, session_id=session_id)
        claims = decode_refresh_token(refresh)
        created = datetime.now(timezone.utc)
        expires = datetime.fromtimestamp(claims["exp"], timezone.utc)
        self.repo.create_session(session_id=session_id, user_id=user.id_user, refresh_token_hash=_hash(refresh), expires_at=expires, created_at=created)
        access = create_access_token(subject=user.email, role=role, session_id=session_id)
        return IssuedTokens(access, refresh, role)

    def refresh(self, refresh_token: str) -> IssuedTokens:
        try:
            claims = decode_refresh_token(refresh_token)
            session_id, email = claims.get("sid"), claims.get("sub")
            if not session_id or not email:
                raise ValueError
        except ValueError as exc:
            raise _unauthorized() from exc
        session = self.repo.get_session(session_id, for_update=True)
        user = self.repo.get_user_by_email(email)
        if not session or not session.is_active() or not user or session.user_id != user.id_user or not secrets.compare_digest(session.refresh_token_hash, _hash(refresh_token)):
            self.db.rollback()
            raise _unauthorized()
        replacement = self._issue_session(user)
        replacement_claims = decode_refresh_token(replacement.refresh_token)
        session.replaced_by_session_id = replacement_claims["sid"]
        session.last_used_at = datetime.now(timezone.utc)
        session.revoke(reason="rotated")
        self.db.commit()
        return replacement

    def logout(self, session_id: str) -> None:
        session = self.repo.get_session(session_id, for_update=True)
        if session and session.is_active():
            session.revoke(reason="logout")
            self.db.commit()
        else:
            self.db.rollback()

    def forgot_password(self, email: str) -> dict:
        key = _rate_key("forgot-password", email)
        if is_rate_limited(key, max_attempts=3):
            raise HTTPException(status_code=429, detail="Too many password reset requests.")
        user = self.repo.get_user_by_email(email)
        if user:
            raw = secrets.token_urlsafe(32)
            reset = PasswordResetToken(user_id=user.id_user, token_hash=_hash(raw), expires_at=datetime.now(timezone.utc) + timedelta(minutes=30), used=False)
            self.db.add(reset)
            self.db.commit()
            try:
                self.email_sender.send_password_reset(email, raw)
            except RuntimeError:
                self.db.delete(reset)
                self.db.commit()
                raise HTTPException(status_code=503, detail="Unable to send password reset email.") from None
            record_attempt(key)
        return {"message": "If the account exists, a password reset link has been sent to the email address."}

    def reset_password(self, token: str, new_password: str) -> dict:
        record = self.db.query(PasswordResetToken).filter(PasswordResetToken.token_hash == _hash(token), PasswordResetToken.used.is_(False)).with_for_update().first()
        now = datetime.now(timezone.utc)
        if not record or _aware(record.expires_at) <= now:
            self.db.rollback()
            raise HTTPException(status_code=400, detail="Invalid or expired reset token.")
        record.user.password = hash_password(new_password)
        record.used = True
        self.repo.revoke_user_sessions(record.user_id, at=now, reason="password_reset")
        self.db.commit()
        return {"message": "Password updated successfully."}

    def google_login(self, email: str):
        user = self.repo.get_user_by_email(email)
        if not user:
            return None
        if str(user.account_status or "").casefold() not in {"ativo", "active"}:
            raise _unauthorized()
        tokens = self._issue_session(user)
        self.db.commit()
        return tokens

    def google_register(self, *, name: str, email: str, cpf: str, phone: str, address_payload) -> tuple[object, int, IssuedTokens]:
        now = datetime.now(timezone.utc)
        if self.repo.get_user_by_email(email):
            raise HTTPException(status_code=409, detail="Registration data is already in use.")
        phone_record = self.repo.verified_phone_code(phone, now)
        if not phone_record:
            self.db.rollback()
            raise HTTPException(status_code=400, detail="Phone verification is required.")
        try:
            registration = Registration.start(email=email, phone=phone)
            registration.verify_email(email)
            registration.verify_phone(phone)
            address = BrazilianAddress(**address_payload.model_dump())
            registration.set_profile(name=name or "Google User", cpf=cpf, address=address)
            registration.set_password_hash(hash_password(secrets.token_urlsafe(32)))
            completed = registration.complete()
            formatted_cpf = str(PersistentCPF(completed.cpf))
            if self.repo.get_user_by_email(email) or self.repo.get_user_by_phone(phone) or self.repo.get_user_by_cpf(formatted_cpf):
                raise HTTPException(status_code=409, detail="Registration data is already in use.")
            user, persisted_address = self.repo.create_user_with_address(
                name=completed.name, email=completed.email, phone=completed.phone,
                cpf=formatted_cpf, password_hash=completed.password_hash,
                address_data={
                    "zip_code": address.zip_code, "state": address.state,
                    "neighborhood": address.neighborhood, "street_name": address.street_name,
                    "number": address.number, "complement": address.complement,
                },
            )
            self.db.delete(phone_record)
            tokens = self._issue_session(user)
            self.db.commit()
            return user, persisted_address.id_address, tokens
        except HTTPException:
            self.db.rollback()
            raise
        except (ValidationException, ValueError) as exc:
            self.db.rollback()
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        except IntegrityError as exc:
            self.db.rollback()
            raise HTTPException(
                status_code=409,
                detail="Registration data is already in use.",
            ) from exc
        except Exception:
            self.db.rollback()
            raise
