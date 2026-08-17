from datetime import datetime, timedelta, timezone

from app.shared.infrastructure.auth.security import hash_password
from app.shared.infrastructure.persistence.auth_session import AuthSession
from app.shared.infrastructure.persistence.user import User


def _user(db_session, email="session@test.com"):
    user = User(
        name="Session User",
        email=email,
        phone="11987654321",
        cpf="529.982.247-25",
        password=hash_password("ValidPass1!"),
        account_status="Ativo",
        type="user",
    )
    db_session.add(user)
    db_session.commit()
    return user


def test_refresh_rotates_and_rejects_reuse(client, db_session):
    _user(db_session)
    login = client.post("/auth/login", json={"email": "session@test.com", "password": "ValidPass1!"})
    assert login.status_code == 200
    first_refresh = login.json()["refresh_token"]

    rotated = client.post("/auth/refresh", json={"refresh_token": first_refresh})
    assert rotated.status_code == 200
    assert rotated.json()["refresh_token"] != first_refresh
    assert client.post("/auth/refresh", json={"refresh_token": first_refresh}).status_code == 401


def test_logout_revokes_access_session(client, db_session):
    _user(db_session)
    tokens = client.post("/auth/login", json={"email": "session@test.com", "password": "ValidPass1!"}).json()
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    assert client.get("/auth/me", headers=headers).status_code == 200
    assert client.post("/auth/logout", headers=headers).status_code == 204
    assert client.get("/auth/me", headers=headers).status_code == 401
    assert client.post("/auth/refresh", json={"refresh_token": tokens["refresh_token"]}).status_code == 401


def test_expired_persisted_session_rejects_access(client, db_session):
    user = _user(db_session)
    tokens = client.post("/auth/login", json={"email": user.email, "password": "ValidPass1!"}).json()
    session = db_session.query(AuthSession).filter(AuthSession.user_id == user.id_user).one()
    session.created_at = datetime.now(timezone.utc) - timedelta(hours=2)
    session.expires_at = datetime.now(timezone.utc) - timedelta(hours=1)
    db_session.commit()
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    assert client.get("/auth/me", headers=headers).status_code == 401


def test_login_does_not_enumerate_unknown_account(client):
    response = client.post("/auth/login", json={"email": "missing@test.com", "password": "ValidPass1!"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials."}
