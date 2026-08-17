from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy import create_engine, event, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.infrastructure.persistence import models  # noqa: F401
from app.shared.infrastructure.database.connection import Base
from app.shared.infrastructure.persistence.auth_session import AuthSession
from app.shared.infrastructure.persistence.cpf import CPF
from app.shared.infrastructure.persistence.phone_verification_code import (
    PhoneVerificationCode,
)
from app.shared.infrastructure.persistence.user import User


@pytest.fixture
def isolated_session():
    engine = create_engine("sqlite:///:memory:")

    @event.listens_for(engine, "connect")
    def enable_foreign_keys(dbapi_connection, _connection_record):
        dbapi_connection.execute("PRAGMA foreign_keys=ON")

    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    Base.metadata.drop_all(engine)
    engine.dispose()


def _user(*, email: str, cpf: str) -> User:
    return User(
        name="Pessoa Teste",
        email=email,
        password="hash",
        cpf=cpf,
        type="user",
    )


def test_cpf_is_one_to_one_queryable_and_cascades(isolated_session):
    user = _user(email="one@example.com", cpf="529.982.247-25")
    isolated_session.add(user)
    isolated_session.commit()

    assert user.cpf == "529.982.247-25"
    assert user.cpf_record.user_id == user.id_user
    assert isolated_session.scalar(
        select(User).where(User.cpf == "529.982.247-25")
    ) is user

    isolated_session.delete(user)
    isolated_session.commit()
    assert isolated_session.scalar(select(CPF)) is None


def test_cpf_number_is_unique(isolated_session):
    isolated_session.add_all(
        [
            _user(email="one@example.com", cpf="529.982.247-25"),
            _user(email="two@example.com", cpf="529.982.247-25"),
        ]
    )

    with pytest.raises(IntegrityError):
        isolated_session.commit()


def test_phone_verification_constraints_and_expiry(isolated_session):
    now = datetime.now(timezone.utc)
    code = PhoneVerificationCode(
        phone="+5511999999999",
        code_hash="hash",
        created_at=now,
        expires_at=now + timedelta(minutes=5),
    )
    isolated_session.add(code)
    isolated_session.commit()

    assert code.verified is False
    assert code.attempt_count == 0
    assert code.is_expired(at=now) is False
    assert code.is_expired(at=now + timedelta(minutes=6)) is True

    code.attempt_count = -1
    with pytest.raises(IntegrityError):
        isolated_session.commit()


def test_auth_session_supports_revocation_and_refresh_rotation(isolated_session):
    now = datetime.now(timezone.utc)
    user = _user(email="session@example.com", cpf="529.982.247-25")
    old_session = AuthSession(
        user=user,
        refresh_token_hash="a" * 64,
        created_at=now,
        expires_at=now + timedelta(days=7),
    )
    replacement = AuthSession(
        user=user,
        refresh_token_hash="b" * 64,
        created_at=now,
        expires_at=now + timedelta(days=7),
    )
    old_session.replacement = replacement
    old_session.revoke(reason="rotated", at=now + timedelta(minutes=1))
    isolated_session.add(user)
    isolated_session.commit()

    assert old_session.is_active(at=now + timedelta(minutes=2)) is False
    assert old_session.revocation_reason == "rotated"
    assert old_session.replaced_by_session_id == replacement.id
    assert replacement.is_active(at=now + timedelta(minutes=2)) is True

    duplicate = AuthSession(
        user=user,
        refresh_token_hash="b" * 64,
        created_at=now,
        expires_at=now + timedelta(days=1),
    )
    isolated_session.add(duplicate)
    with pytest.raises(IntegrityError):
        isolated_session.commit()
