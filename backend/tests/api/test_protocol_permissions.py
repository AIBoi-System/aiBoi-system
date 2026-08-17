from app.enums.protocol.protocol_status import ProtocolStatus
from app.enums.reproduction.reproduction_type import ReproductionType


def test_owner_can_read_but_cannot_modify_global_protocol_catalog(client, auth_setup):
    headers = auth_setup["headers"]

    read_response = client.get("/reproductions/protocols", headers=headers)
    assert read_response.status_code == 200

    write_response = client.post(
        "/reproductions/protocols",
        headers=headers,
        json={
            "name": "IATF global",
            "type": ReproductionType.IATF.value,
            "status": ProtocolStatus.NOT_STARTED.value,
        },
    )
    assert write_response.status_code == 403


def test_protocol_catalog_requires_authentication(client):
    response = client.get("/reproductions/protocols")

    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"
