from datetime import datetime, timedelta, timezone

from app.shared.infrastructure.persistence.email_verification_code import EmailVerificationCode
from app.shared.infrastructure.persistence.user import User


def test_signup_requires_both_one_time_verifications(client, monkeypatch):
    monkeypatch.setattr("app.shared.application.auth.auth_service._generate_code", lambda: "12345")
    email = "new.signup@test.com"
    phone = "11987654321"
    email_send = client.post("/auth/signup/send-code", json={"email": email})
    phone_send = client.post("/auth/signup/send-phone-code", json={"phone": phone})
    assert email_send.status_code == phone_send.status_code == 200
    assert "12345" not in str(email_send.json())
    assert "12345" not in str(phone_send.json())
    assert client.post("/auth/signup/verify-code", json={"email": email, "code": "12345"}).status_code == 200
    assert client.post("/auth/signup/verify-phone-code", json={"phone": phone, "code": "12345"}).status_code == 200

    payload = {
        "name": "Secure Signup", "email": email, "phone": phone,
        "password": "ValidPass1!", "cpf": "52998224725",
        "address": {"zip_code": "01001000", "state": "SP", "neighborhood": "Centro", "street_name": "Rua Segura", "number": "10"},
    }
    created = client.post("/auth/signup/register", json=payload)
    assert created.status_code == 201
    assert client.post("/auth/signup/register", json=payload).status_code == 400


def test_expired_email_code_is_rejected(client, db_session):
    from app.shared.application.auth.auth_service import _hash

    db_session.add(EmailVerificationCode(
        email="expired@test.com", code_hash=_hash("12345"), verified=False,
        expires_at=datetime.now(timezone.utc) - timedelta(minutes=1),
    ))
    db_session.commit()
    response = client.post("/auth/signup/verify-code", json={"email": "expired@test.com", "code": "12345"})
    assert response.status_code == 400


def test_send_code_response_does_not_enumerate_registered_email(client, db_session):
    db_session.add(User(name="Existing", email="existing-enum@test.com", phone=None, cpf="111.444.777-35", password="unused", type="user"))
    db_session.commit()
    existing = client.post("/auth/signup/send-code", json={"email": "existing-enum@test.com"})
    unknown = client.post("/auth/signup/send-code", json={"email": "unknown-enum@test.com"})
    assert existing.status_code == unknown.status_code == 200
    assert existing.json() == unknown.json()
