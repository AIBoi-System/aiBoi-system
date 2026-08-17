import pytest
from datetime import date
from app.enums.animal.animal_category import AnimalCategory
from app.enums.animal.animal_life_status import AnimalLifeStatus
from app.enums.animal.animal_origin import AnimalOrigin
from app.enums.animal.animal_sex import AnimalSex
from app.enums.animal.animal_size import AnimalSize
from app.shared.infrastructure.persistence.owner import Owner
from app.shared.infrastructure.persistence.property import Property
from app.enums.property.property_type import PropertyType
from app.enums.owner.owner_subscription_status import OwnerSubscriptionStatus
from app.shared.infrastructure.auth.auth import create_access_token
from app.modules.inventory.infrastructure.persistence.animal import AnimalModel


@pytest.fixture
def weighing_test_data(db_session, auth_setup):
    # Criar um animal na propriedade do Proprietário A (auth_setup)
    prop_a = auth_setup["property"]
    animal_a = AnimalModel(
        identification_number=8001,
        sex=AnimalSex.M,
        animal_size=AnimalSize.MEDIUM_SIZE,
        animal_life_status=AnimalLifeStatus.ACTIVE,
        animal_category=AnimalCategory.BULL,
        birth_date=date(2023, 1, 1),
        origin=AnimalOrigin.PURCHASE,
        property_id=prop_a.id_property
    )
    db_session.add(animal_a)
    db_session.commit()
    db_session.refresh(animal_a)

    # Proprietário B e sua propriedade B
    owner_b = Owner(
        name="Owner B",
        email="owner_b_weigh@example.com",
        password="hash_password",
        cpf="888.888.888-88",
        type="owner",
        subscription_status=OwnerSubscriptionStatus.FREE
    )
    db_session.add(owner_b)
    db_session.commit()
    db_session.refresh(owner_b)

    prop_b = Property(
        name="Fazenda B",
        property_type=PropertyType.BEEF,
        area=150.0,
        owner_id=owner_b.id_user
    )
    db_session.add(prop_b)
    db_session.commit()
    db_session.refresh(prop_b)

    # Criar um animal pertencente ao Proprietário B
    animal_b = AnimalModel(
        identification_number=8002,
        sex=AnimalSex.M,
        animal_size=AnimalSize.MEDIUM_SIZE,
        animal_life_status=AnimalLifeStatus.ACTIVE,
        animal_category=AnimalCategory.BULL,
        birth_date=date(2023, 1, 1),
        origin=AnimalOrigin.PURCHASE,
        property_id=prop_b.id_property
    )
    db_session.add(animal_b)
    db_session.commit()
    db_session.refresh(animal_b)

    return {
        "animal_a": animal_a,
        "animal_b": animal_b,
        "token_b": create_access_token(owner_b.email, "owner"),
        "headers_b": {"Authorization": f"Bearer {create_access_token(owner_b.email, 'owner')}"}
    }


def test_create_and_list_weighing_success(client, auth_setup, weighing_test_data):
    headers = auth_setup["headers"]
    property_id = auth_setup["property"].id_property
    animal_a = weighing_test_data["animal_a"]

    # 1. Registrar pesagem
    payload = {
        "weight": 420.5,
        "animal_id": animal_a.id_animal,
        "weigh_date": date.today().isoformat()
    }
    resp = client.post(
        f"/weighings/?property_id={property_id}", json=payload, headers=headers
    )
    assert resp.status_code == 201
    created = resp.json()
    assert created["weight"] == 420.5
    assert created["animal_id"] == animal_a.id_animal
    weighing_id = created["id"]

    # 2. Listar histórico por animal
    list_resp = client.get(
        f"/weighings/animal/{animal_a.id_animal}?property_id={property_id}",
        headers=headers,
    )
    assert list_resp.status_code == 200
    assert len(list_resp.json()) == 1
    assert list_resp.json()[0]["id"] == weighing_id

    update_resp = client.put(
        f"/weighings/{weighing_id}?property_id={property_id}",
        json={"weight": 430.0},
        headers=headers,
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["weight"] == 430.0

    delete_resp = client.delete(
        f"/weighings/{weighing_id}?property_id={property_id}", headers=headers
    )
    assert delete_resp.status_code == 204


def test_weighing_cross_tenant_denied(client, auth_setup, weighing_test_data):
    headers_a = auth_setup["headers"]
    headers_b = weighing_test_data["headers_b"]
    animal_a = weighing_test_data["animal_a"]
    animal_b = weighing_test_data["animal_b"]
    property_a_id = auth_setup["property"].id_property
    property_b_id = animal_b.property_id

    # Usuário B tenta pesar animal A (de propriedade A) -> deve ser negado com 404
    payload_invalid = {
        "weight": 450.0,
        "animal_id": animal_a.id_animal,
        "weigh_date": date.today().isoformat()
    }
    resp = client.post(
        f"/weighings/?property_id={property_b_id}",
        json=payload_invalid,
        headers=headers_b,
    )
    assert resp.status_code == 404

    # Usuário B tenta listar histórico do animal A -> deve ser negado com 404
    resp_get = client.get(
        f"/weighings/animal/{animal_a.id_animal}?property_id={property_b_id}",
        headers=headers_b,
    )
    assert resp_get.status_code == 404

    owner_create = client.post(
        f"/weighings/?property_id={property_a_id}",
        json=payload_invalid,
        headers=headers_a,
    )
    assert owner_create.status_code == 201
    weighing_id = owner_create.json()["id"]

    assert client.put(
        f"/weighings/{weighing_id}?property_id={property_a_id}",
        json={"weight": 999.0},
        headers=headers_b,
    ).status_code == 404
    assert client.delete(
        f"/weighings/{weighing_id}?property_id={property_a_id}",
        headers=headers_b,
    ).status_code == 404
