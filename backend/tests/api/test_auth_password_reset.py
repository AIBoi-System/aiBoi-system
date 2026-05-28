def test_password_reset_flow(client):
    user_payload = {
        "name": "Sandro",
        "email": "sandro@test.com",
        "phone": "999999999",
        "cpf": "52998224725",
        "address_id": None,
        "password": "12345678",
    }
    create_resp = client.post("/users/", json=user_payload)
    assert create_resp.status_code == 200

    login_resp = client.post(
        "/auth/login",
        json={"email": "sandro@test.com", "password": "12345678"},
    )
    assert login_resp.status_code == 200
    assert "access_token" in login_resp.json()

    forgot_resp = client.post(
        "/auth/forgot-password",
        json={"email": "sandro@test.com"},
    )
    assert forgot_resp.status_code == 200
    reset_token = forgot_resp.json()["reset_token"]

    reset_resp = client.post(
        "/auth/reset-password",
        json={"token": reset_token, "new_password": "newpassword123"},
    )
    assert reset_resp.status_code == 200

    old_login = client.post(
        "/auth/login",
        json={"email": "sandro@test.com", "password": "12345678"},
    )
    assert old_login.status_code == 401

    new_login = client.post(
        "/auth/login",
        json={"email": "sandro@test.com", "password": "newpassword123"},
    )
    assert new_login.status_code == 200
