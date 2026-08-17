import pytest
from datetime import date
from app.enums.animal.animal_category import AnimalCategory
from app.enums.animal.animal_life_status import AnimalLifeStatus
from app.enums.animal.animal_origin import AnimalOrigin
from app.enums.animal.animal_sex import AnimalSex
from app.enums.animal.animal_size import AnimalSize
from app.enums.animal.animal_reproductive_status import AnimalReproductiveStatus
from app.enums.reproduction.reproduction_type import ReproductionType
from app.enums.reproduction.reproduction_status import ReproductionStatus
from app.shared.infrastructure.persistence.owner import Owner
from app.shared.infrastructure.persistence.property import Property
from app.enums.property.property_type import PropertyType
from app.enums.owner.owner_subscription_status import OwnerSubscriptionStatus
from app.shared.infrastructure.auth.auth import create_access_token
from app.modules.inventory.infrastructure.persistence.animal import AnimalModel


@pytest.fixture
def reproduction_test_data(db_session, auth_setup):
    # Criar uma fêmea na propriedade do Proprietário A (auth_setup)
    prop_a = auth_setup["property"]
    animal_a = AnimalModel(
        identification_number=9001,
        sex=AnimalSex.F,
        animal_size=AnimalSize.MEDIUM_SIZE,
        animal_life_status=AnimalLifeStatus.ACTIVE,
        animal_category=AnimalCategory.HEIFER,
        reproductive_status=AnimalReproductiveStatus.OPEN,
        birth_date=date(2022, 1, 1),
        origin=AnimalOrigin.BIRTH,
        property_id=prop_a.id_property
    )
    db_session.add(animal_a)
    db_session.commit()
    db_session.refresh(animal_a)

    # Proprietário B e sua propriedade B
    owner_b = Owner(
        name="Owner B Repro",
        email="owner_b_repro@example.com",
        password="hash_password",
        cpf="777.777.777-77",
        type="owner",
        subscription_status=OwnerSubscriptionStatus.FREE
    )
    db_session.add(owner_b)
    db_session.commit()
    db_session.refresh(owner_b)

    prop_b = Property(
        name="Fazenda B Repro",
        property_type=PropertyType.BEEF,
        area=100.0,
        owner_id=owner_b.id_user
    )
    db_session.add(prop_b)
    db_session.commit()
    db_session.refresh(prop_b)

    # Criar uma fêmea pertencente ao Proprietário B
    animal_b = AnimalModel(
        identification_number=9002,
        sex=AnimalSex.F,
        animal_size=AnimalSize.MEDIUM_SIZE,
        animal_life_status=AnimalLifeStatus.ACTIVE,
        animal_category=AnimalCategory.HEIFER,
        reproductive_status=AnimalReproductiveStatus.OPEN,
        birth_date=date(2022, 1, 1),
        origin=AnimalOrigin.BIRTH,
        property_id=prop_b.id_property
    )
    db_session.add(animal_b)
    db_session.commit()
    db_session.refresh(animal_b)

    # Token de B
    token_b = create_access_token(owner_b.email, "owner")
    headers_b = {"Authorization": f"Bearer {token_b}"}

    return {
        "animal_a": animal_a,
        "animal_b": animal_b,
        "prop_b": prop_b,
        "headers_b": headers_b
    }


def test_reproduction_flow_success(client, auth_setup, reproduction_test_data):
    headers = auth_setup["headers"]
    prop_a = auth_setup["property"]
    animal_a = reproduction_test_data["animal_a"]

    # 1. Registrar reprodução
    payload = {
        "reproduction_type": ReproductionType.MONTA_NATURAL.value,
        "reproduction_status": ReproductionStatus.IN_PROGRESS.value,
        "start_date": date.today().isoformat(),
        "animal_id": animal_a.id_animal,
        "notes": "Monta de teste"
    }
    resp = client.post(f"/reproductions/?property_id={prop_a.id_property}", json=payload, headers=headers)
    assert resp.status_code == 201
    repro = resp.json()
    assert repro["notes"] == "Monta de teste"
    repro_id = repro["id"]

    # 2. Listar reproduções
    list_resp = client.get(f"/reproductions/?property_id={prop_a.id_property}", headers=headers)
    assert list_resp.status_code == 200
    assert len(list_resp.json()) >= 1
    assert any(r["id"] == repro_id for r in list_resp.json())

    # 3. Registrar nascimento
    birth_payload = {
        "birth_date": date.today().isoformat(),
        "calf_alive": True,
        "calf_sex": "M",
        "calf_category": "Bezerro",
        "notes": "Bezerro forte"
    }
    birth_resp = client.post(f"/reproductions/{repro_id}/birth?property_id={prop_a.id_property}", json=birth_payload, headers=headers)
    assert birth_resp.status_code == 200
    assert birth_resp.json()["reproduction_status"] == ReproductionStatus.COMPLETED.value


def test_reproduction_cross_tenant_denied(client, auth_setup, reproduction_test_data):
    headers_b = reproduction_test_data["headers_b"]
    prop_b = reproduction_test_data["prop_b"]
    animal_a = reproduction_test_data["animal_a"]

    # Usuário B tenta criar reprodução para o animal A (de propriedade A) com property_id = B -> deve falhar com 404
    payload_invalid = {
        "reproduction_type": ReproductionType.MONTA_NATURAL.value,
        "reproduction_status": ReproductionStatus.IN_PROGRESS.value,
        "start_date": date.today().isoformat(),
        "animal_id": animal_a.id_animal,
        "notes": "Tentativa invasiva"
    }
    resp = client.post(f"/reproductions/?property_id={prop_b.id_property}", json=payload_invalid, headers=headers_b)
    assert resp.status_code == 404
