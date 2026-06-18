from datetime import date

import pytest

from app.enums.animal.animal_category import AnimalCategory
from app.enums.animal.animal_life_status import AnimalLifeStatus
from app.enums.animal.animal_origin import AnimalOrigin
from app.enums.animal.animal_sex import AnimalSex
from app.enums.animal.animal_size import AnimalSize


@pytest.fixture
def animal_payload():
    return {
        "identification_number": 1001,
        "sex": AnimalSex.F.value,
        "animal_size": AnimalSize.MEDIUM_SIZE.value,
        "animal_life_status": AnimalLifeStatus.ACTIVE.value,
        "animal_category": AnimalCategory.HEIFER.value,
        "birth_date": date(2022, 3, 15).isoformat(),
        "origin": AnimalOrigin.BIRTH.value,
        "name": "Mimosa",
    }


def test_create_and_get_animal(client, animal_payload):
    create_resp = client.post("/animals/", json=animal_payload)
    assert create_resp.status_code == 201
    created = create_resp.json()
    assert created["identification_number"] == 1001
    assert created["name"] == "Mimosa"
    animal_id = created["id_animal"]

    get_resp = client.get(f"/animals/{animal_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["id_animal"] == animal_id


def test_list_animals(client, animal_payload):
    client.post("/animals/", json=animal_payload)
    animal_payload["identification_number"] = 1002
    client.post("/animals/", json=animal_payload)

    list_resp = client.get("/animals/")
    assert list_resp.status_code == 200
    assert len(list_resp.json()) >= 2


def test_duplicate_identification_returns_400(client, animal_payload):
    client.post("/animals/", json=animal_payload)
    dup_resp = client.post("/animals/", json=animal_payload)
    assert dup_resp.status_code == 400


def test_get_animal_not_found(client):
    response = client.get("/animals/99999")
    assert response.status_code == 404


def test_update_animal(client, animal_payload):
    create_resp = client.post("/animals/", json=animal_payload)
    animal_id = create_resp.json()["id_animal"]

    update_resp = client.put(
        f"/animals/{animal_id}",
        json={"name": "Mimosa Atualizada"},
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["name"] == "Mimosa Atualizada"



