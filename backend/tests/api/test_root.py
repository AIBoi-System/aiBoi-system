def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "Online"
    assert data["projeto"] == "AiBoi"
    assert "arquitetura" in data


def test_test_db_sqlite(client):
    response = client.get("/test-db")
    assert response.status_code == 200
    assert response.json()["status"] == "sucesso"



