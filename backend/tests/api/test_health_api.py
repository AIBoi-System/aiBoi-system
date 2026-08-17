from datetime import date

import pytest

from app.enums.animal.animal_category import AnimalCategory
from app.enums.animal.animal_life_status import AnimalLifeStatus
from app.enums.animal.animal_origin import AnimalOrigin
from app.enums.animal.animal_sex import AnimalSex
from app.enums.animal.animal_size import AnimalSize
from app.enums.health.health_type import HealthType


@pytest.fixture
def animal_id(client, auth_setup):
    payload = {
        "identification_number": 2001,
        "sex": AnimalSex.M.value,
        "animal_size": AnimalSize.MEDIUM_SIZE.value,
        "animal_life_status": AnimalLifeStatus.ACTIVE.value,
        "animal_category": AnimalCategory.BULL.value,
        "birth_date": date(2021, 1, 10).isoformat(),
        "origin": AnimalOrigin.PURCHASE.value,
    }
    prop_id = auth_setup["property"].id_property
    response = client.post(
        f"/animals/?property_id={prop_id}",
        json=payload,
        headers=auth_setup["headers"],
    )
    return response.json()["id_animal"]


@pytest.fixture
def health_payload(animal_id, auth_setup):
    return {
        "health_type": HealthType.VACCINE.value,
        "product_name": "Vacina Aftosa",
        "application_date": date.today().isoformat(),
        "animal_id": animal_id,
        "responsible": "Dr. Silva",
        "property_id": auth_setup["property"].id_property,
    }


def test_create_health_record(client, health_payload, auth_setup):
    response = client.post(
        "/health/",
        json=health_payload,
        headers=auth_setup["headers"],
    )
    assert response.status_code == 201
    data = response.json()
    assert data["product_name"] == "Vacina Aftosa"
    assert data["animal_id"] == health_payload["animal_id"]


def test_health_requires_target(client, auth_setup):
    response = client.post(
        "/health/",
        json={
            "health_type": HealthType.VACCINE.value,
            "product_name": "Sem alvo",
            "application_date": date.today().isoformat(),
            "property_id": auth_setup["property"].id_property,
        },
        headers=auth_setup["headers"],
    )
    assert response.status_code == 400


def test_list_and_delete_health(client, health_payload, auth_setup):
    create_resp = client.post(
        "/health/",
        json=health_payload,
        headers=auth_setup["headers"],
    )
    assert create_resp.status_code == 201
    health_id = create_resp.json()["id_health_record"]
    prop_id = auth_setup["property"].id_property

    list_resp = client.get(
        f"/health/?property_id={prop_id}",
        headers=auth_setup["headers"],
    )
    assert list_resp.status_code == 200
    assert any(h["id_health_record"] == health_id for h in list_resp.json())

    delete_resp = client.delete(
        f"/health/{health_id}?property_id={prop_id}",
        headers=auth_setup["headers"],
    )
    assert delete_resp.status_code == 204

    get_resp = client.get(
        f"/health/{health_id}?property_id={prop_id}",
        headers=auth_setup["headers"],
    )
    assert get_resp.status_code == 404



