from __future__ import annotations

from datetime import datetime

from sqlalchemy.orm import Session

from app.shared.infrastructure.persistence.address import Address
from app.shared.infrastructure.persistence.auth_session import AuthSession
from app.shared.infrastructure.persistence.cpf import CPF
from app.shared.infrastructure.persistence.email_verification_code import (
    EmailVerificationCode,
)
from app.shared.infrastructure.persistence.phone_verification_code import (
    PhoneVerificationCode,
)
from app.shared.infrastructure.persistence.user import User


class AuthRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_user_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_phone(self, phone: str) -> User | None:
        return self.db.query(User).filter(User.phone == phone).first()

    def get_user_by_cpf(self, cpf: str) -> User | None:
        return self.db.query(User).join(CPF).filter(CPF.number == cpf).first()

    def replace_pending_email_code(self, record: EmailVerificationCode) -> None:
        self.db.query(EmailVerificationCode).filter(
            EmailVerificationCode.email == record.email,
            EmailVerificationCode.verified.is_(False),
        ).delete(synchronize_session=False)
        self.db.add(record)

    def latest_email_code(self, email: str) -> EmailVerificationCode | None:
        return (
            self.db.query(EmailVerificationCode)
            .filter(EmailVerificationCode.email == email)
            .order_by(EmailVerificationCode.created_at.desc())
            .with_for_update()
            .first()
        )

    def replace_pending_phone_code(self, record: PhoneVerificationCode) -> None:
        self.db.query(PhoneVerificationCode).filter(
            PhoneVerificationCode.phone == record.phone,
            PhoneVerificationCode.verified.is_(False),
        ).delete(synchronize_session=False)
        self.db.add(record)

    def latest_phone_code(self, phone: str) -> PhoneVerificationCode | None:
        return (
            self.db.query(PhoneVerificationCode)
            .filter(PhoneVerificationCode.phone == phone)
            .order_by(PhoneVerificationCode.created_at.desc())
            .with_for_update()
            .first()
        )

    def verified_email_code(
        self, email: str, now: datetime
    ) -> EmailVerificationCode | None:
        return (
            self.db.query(EmailVerificationCode)
            .filter(
                EmailVerificationCode.email == email,
                EmailVerificationCode.verified.is_(True),
                EmailVerificationCode.expires_at > now,
            )
            .order_by(EmailVerificationCode.created_at.desc())
            .with_for_update()
            .first()
        )

    def verified_phone_code(
        self, phone: str, now: datetime
    ) -> PhoneVerificationCode | None:
        return (
            self.db.query(PhoneVerificationCode)
            .filter(
                PhoneVerificationCode.phone == phone,
                PhoneVerificationCode.verified.is_(True),
                PhoneVerificationCode.expires_at > now,
            )
            .order_by(PhoneVerificationCode.created_at.desc())
            .with_for_update()
            .first()
        )

    def consume_verifications(
        self,
        email_record: EmailVerificationCode,
        phone_record: PhoneVerificationCode,
    ) -> None:
        self.db.delete(email_record)
        self.db.delete(phone_record)

    def create_user_with_address(
        self,
        *,
        name: str,
        email: str,
        phone: str,
        cpf: str,
        password_hash: str,
        address_data: dict,
    ) -> tuple[User, Address]:
        address = Address(**address_data)
        self.db.add(address)
        self.db.flush()
        user = User(
            name=name,
            email=email,
            phone=phone,
            cpf=cpf,
            password=password_hash,
            address_id=address.id_address,
            account_status="Ativo",
            type="user",
        )
        self.db.add(user)
        self.db.flush()
        return user, address

    def create_session(
        self,
        *,
        session_id: str,
        user_id: int,
        refresh_token_hash: str,
        expires_at: datetime,
        created_at: datetime,
    ) -> AuthSession:
        session = AuthSession(
            id=session_id,
            user_id=user_id,
            refresh_token_hash=refresh_token_hash,
            created_at=created_at,
            expires_at=expires_at,
        )
        self.db.add(session)
        self.db.flush()
        return session

    def get_session(
        self, session_id: str, *, for_update: bool = False
    ) -> AuthSession | None:
        query = self.db.query(AuthSession).filter(AuthSession.id == session_id)
        if for_update:
            query = query.with_for_update()
        return query.first()

    def revoke_user_sessions(
        self, user_id: int, *, at: datetime, reason: str
    ) -> None:
        sessions = self.db.query(AuthSession).filter(
            AuthSession.user_id == user_id,
            AuthSession.revoked_at.is_(None),
        )
        for session in sessions:
            session.revoke(reason=reason, at=at)
