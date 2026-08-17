from unittest.mock import patch
from app.shared.infrastructure.persistence.user import User
from app.shared.infrastructure.auth.security import hash_password
from app.shared.infrastructure.persistence.phone_verification_code import PhoneVerificationCode
from datetime import datetime, timedelta, timezone

@patch("app.presentation.api.v1.auth_router.verify_google_token")
def test_google_login_needs_registration(mock_verify, client):
    mock_verify.return_value = {
        "email": "newgoogleuser@test.com",
        "name": "New Google User",
        "email_verified": True,
    }

    resp = client.post(
        "/auth/login/google",
        json={"id_token": "dummy_token_123"}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["needs_registration"] is True
    assert data["email"] == "newgoogleuser@test.com"
    assert data["name"] == "New Google User"
    assert data["access_token"] is None


@patch("app.presentation.api.v1.auth_router.verify_google_token")
def test_google_login_success(mock_verify, client, db_session):
    user = User(
        name="Existing Google User",
        email="existinggoogle@test.com",
        phone="11999999999",
        cpf="12345678901",
        address_id=None,
        password=hash_password("12345678"),
        type="user"
    )
    db_session.add(user)
    db_session.commit()

    mock_verify.return_value = {
        "email": "existinggoogle@test.com",
        "name": "Existing Google User",
        "email_verified": True,
    }

    resp = client.post(
        "/auth/login/google",
        json={"id_token": "dummy_token_123"}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["needs_registration"] is False
    assert data["access_token"] is not None
    assert data["role"] == "user"


@patch("app.presentation.api.v1.auth_router.verify_google_token")
def test_google_register_success(mock_verify, client, db_session):
    mock_verify.return_value = {
        "email": "registergoogle@test.com",
        "name": "Register Google User",
        "email_verified": True,
    }
    db_session.add(PhoneVerificationCode(
        phone="11999999999", code_hash="consumed-after-registration",
        expires_at=datetime.now(timezone.utc) + timedelta(hours=1), verified=True,
    ))
    db_session.commit()

    payload = {
        "id_token": "dummy_token_123",
        "cpf": "52998224725",
        "phone": "11999999999",
        "address": {
            "zip_code": "01001000",
            "state": "SP",
            "neighborhood": "Centro",
            "street_name": "Praça da Sé",
            "number": "100",
            "complement": "Apto 1"
        }
    }

    resp = client.post(
        "/auth/register/google",
        json=payload
    )
    assert resp.status_code == 201

    data = resp.json()
    assert "access_token" in data
    assert data["role"] == "user"
    assert data["user_id"] is not None
    assert data["address_id"] is not None

    user = db_session.query(User).filter(User.email == "registergoogle@test.com").first()
    assert user is not None
    assert user.name == "Register Google User"
    assert "".join(filter(str.isdigit, user.cpf)) == "52998224725"


@patch("app.presentation.api.v1.auth_router.verify_google_token")
def test_google_register_already_exists(mock_verify, client, db_session):
    user = User(
        name="Existing Google User",
        email="existinggoogle@test.com",
        phone="11999999999",
        cpf="12345678901",
        address_id=None,
        password=hash_password("12345678"),
        type="user"
    )
    db_session.add(user)
    db_session.commit()

    mock_verify.return_value = {
        "email": "existinggoogle@test.com",
        "name": "Existing Google User",
        "email_verified": True,
    }

    payload = {
        "id_token": "dummy_token_123",
        "cpf": "52998224725",
        "phone": "11999999999",
        "address": {
            "zip_code": "01001000",
            "state": "SP",
            "neighborhood": "Centro",
            "street_name": "Praça da Sé",
            "number": "100"
        }
    }

    resp = client.post(
        "/auth/register/google",
        json=payload
    )
    assert resp.status_code in {400, 409}


@patch("app.presentation.api.v1.auth_router.id_token.verify_oauth2_token")
def test_google_token_verification_failure(mock_verify, client):
    mock_verify.side_effect = ValueError("Invalid token signature")

    resp = client.post(
        "/auth/login/google",
        json={"id_token": "invalid_token"}
    )
    assert resp.status_code == 401
    assert "verification failed" in resp.json()["detail"]
