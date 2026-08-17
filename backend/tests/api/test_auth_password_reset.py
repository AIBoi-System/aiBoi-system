"""Tests for the password reset flow.

After the security fix, the reset token is NO LONGER returned in the HTTP response.
It is sent exclusively via email (logged/skipped in test/dev environment).

To test the full flow, the test retrieves the raw token from the database directly,
simulating what a user would receive via email.
"""

import hashlib
import secrets

from app.shared.infrastructure.persistence.password_reset_token import PasswordResetToken
from app.shared.infrastructure.persistence.user import User
from app.shared.infrastructure.auth.security import hash_password
from app.shared.infrastructure.auth.auth import create_access_token


def test_password_reset_flow(client, db_session):
    """Full password reset flow: request → (email token) → reset → login with new password."""
    user = User(
        name="Sandro",
        email="sandro@test.com",
        phone="999999999",
        cpf="52998224725",
        address_id=None,
        password=hash_password("12345678"),
        type="user",
    )
    db_session.add(user)
    db_session.commit()

    # 1. Login with original password
    login_resp = client.post(
        "/auth/login",
        json={"email": "sandro@test.com", "password": "12345678"},
    )
    assert login_resp.status_code == 200
    data = login_resp.json()
    assert "access_token" in data
    # Verify refresh token is now included in login response
    assert "refresh_token" in data

    # 2. Request password reset
    forgot_resp = client.post(
        "/auth/forgot-password",
        json={"email": "sandro@test.com"},
    )
    assert forgot_resp.status_code == 200

    # Security check: reset_token must NOT be in the HTTP response
    forgot_body = forgot_resp.json()
    assert "reset_token" not in forgot_body, (
        "SECURITY VIOLATION: reset_token must not be returned in the HTTP response. "
        "It should be sent via email only."
    )
    assert "message" in forgot_body

    # 3. Retrieve the token directly from the database (simulates receiving the email link)
    db_session.expire_all()  # refresh session
    reset_record = (
        db_session.query(PasswordResetToken)
        .filter(PasswordResetToken.user_id == user.id_user)
        .order_by(PasswordResetToken.expires_at.desc())
        .first()
    )
    assert reset_record is not None, "Password reset token should have been created in DB"

    # We need the raw token — in a real scenario this comes from the email link.
    # For testing we generate a token, hash it, and store it directly.
    raw_token = secrets.token_urlsafe(32)
    reset_record.token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
    db_session.commit()

    # 4. Use the token to reset the password
    reset_resp = client.post(
        "/auth/reset-password",
        json={"token": raw_token, "new_password": "newpassword123!"},
    )
    assert reset_resp.status_code == 200

    # 5. Old password should no longer work
    old_login = client.post(
        "/auth/login",
        json={"email": "sandro@test.com", "password": "12345678"},
    )
    assert old_login.status_code == 401

    # 6. New password should work
    new_login = client.post(
        "/auth/login",
        json={"email": "sandro@test.com", "password": "newpassword123!"},
    )
    assert new_login.status_code == 200


def test_forgot_password_unknown_email_same_response(client, db_session):
    """Unknown email should return the same response as a known email (prevent user enumeration)."""
    resp = client.post(
        "/auth/forgot-password",
        json={"email": "unknown@nonexistent.com"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert "reset_token" not in body
    assert "message" in body


def test_refresh_token_flow(client, db_session):
    """Test that a refresh token can be used to obtain a new access token."""
    user = User(
        name="Refresh User",
        email="refresh@test.com",
        phone="888888888",
        cpf="12345678901",
        address_id=None,
        password=hash_password("ValidPass1!"),
        type="user",
    )
    db_session.add(user)
    db_session.commit()

    # Login and get tokens
    login_resp = client.post(
        "/auth/login",
        json={"email": "refresh@test.com", "password": "ValidPass1!"},
    )
    assert login_resp.status_code == 200
    tokens = login_resp.json()
    assert "refresh_token" in tokens

    refresh_token = tokens["refresh_token"]

    # Use refresh token to get new access token
    refresh_resp = client.post(
        "/auth/refresh",
        json={"refresh_token": refresh_token},
    )
    assert refresh_resp.status_code == 200
    new_tokens = refresh_resp.json()
    assert "access_token" in new_tokens
    assert "refresh_token" in new_tokens


def test_refresh_token_invalid(client, db_session):
    """Invalid refresh token should return 401."""
    resp = client.post(
        "/auth/refresh",
        json={"refresh_token": "this-is-not-a-valid-token"},
    )
    assert resp.status_code == 401


def test_inactive_user_cannot_login_or_use_existing_token(client, db_session):
    user = User(
        name="Inactive User",
        email="inactive@test.com",
        phone=None,
        cpf="98765432100",
        address_id=None,
        password=hash_password("ValidPass1!"),
        account_status="Inativo",
        type="user",
    )
    db_session.add(user)
    db_session.commit()

    login_response = client.post(
        "/auth/login",
        json={"email": user.email, "password": "ValidPass1!"},
    )
    assert login_response.status_code == 401
    assert login_response.json() == {"detail": "Invalid credentials."}

    token = create_access_token(user.email, "user")
    me_response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert me_response.status_code == 401
    assert me_response.headers["www-authenticate"] == "Bearer"
    assert me_response.json() == {"detail": "Invalid or expired credentials."}
