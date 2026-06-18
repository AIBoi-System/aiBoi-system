from datetime import date

import pytest

from app.enums.animal.animal_category import AnimalCategory
from app.enums.animal.animal_life_status import AnimalLifeStatus
from app.enums.animal.animal_origin import AnimalOrigin
from app.enums.animal.animal_sex import AnimalSex
from app.enums.animal.animal_size import AnimalSize
from app.enums.health.health_type import HealthType


@pytest.fixture
def animal_id(client):
    payload = {
        "identification_number": 2001,
        "sex": AnimalSex.M.value,
        "animal_size": AnimalSize.MEDIUM_SIZE.value,
        "animal_life_status": AnimalLifeStatus.ACTIVE.value,
        "animal_category": AnimalCategory.BULL.value,
        "birth_date": date(2021, 1, 10).isoformat(),
        "origin": AnimalOrigin.PURCHASE.value,
    }
    response = client.post("/animals/", json=payload)
    return response.json()["id_animal"]


@pytest.fixture
def health_payload(animal_id):
    return {
        "health_type": HealthType.VACCINE.value,
        "product_name": "Vacina Aftosa",
        "application_date": date.today().isoformat(),
        "animal_id": animal_id,
        "responsible": "Dr. Silva",
    }


def test_create_health_record(client, health_payload):
    response = client.post("/health/", json=health_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["product_name"] == "Vacina Aftosa"
    assert data["animal_id"] == health_payload["animal_id"]


def test_health_requires_target(client):
    response = client.post(
        "/health/",
        json={
            "health_type": HealthType.VACCINE.value,
            "product_name": "Sem alvo",
            "application_date": date.today().isoformat(),
        },
    )
    assert response.status_code == 400


def test_list_and_delete_health(client, health_payload):
    create_resp = client.post("/health/", json=health_payload)
    health_id = create_resp.json()["id_health_record"]

    list_resp = client.get("/health/")
    assert list_resp.status_code == 200
    assert any(h["id_health_record"] == health_id for h in list_resp.json())

    delete_resp = client.delete(f"/health/{health_id}")
    assert delete_resp.status_code == 200

    get_resp = client.get(f"/health/{health_id}")
    assert get_resp.status_code == 404



