import pytest
from datetime import date
from app.shared.infrastructure.auth.auth import create_access_token
from app.shared.infrastructure.persistence.owner import Owner
from app.shared.infrastructure.persistence.property import Property
from app.modules.inventory.infrastructure.persistence.animal import AnimalModel
from app.modules.inventory.infrastructure.persistence.weighing import Weighing
from app.modules.health.infrastructure.persistence.health import HealthModel
from app.enums.property.property_type import PropertyType
from app.enums.owner.owner_subscription_status import OwnerSubscriptionStatus
from app.enums.health.health_type import HealthType
from app.enums.animal.animal_category import AnimalCategory
from app.enums.animal.animal_life_status import AnimalLifeStatus
from app.enums.animal.animal_origin import AnimalOrigin
from app.enums.animal.animal_sex import AnimalSex
from app.enums.animal.animal_size import AnimalSize

@pytest.fixture
def dashboard_test_data(db_session):
    # Proprietário A
    owner_a = Owner(
        name="Owner A",
        email="owner_a@example.com",
        password="password_hash",
        cpf="333.333.333-33",
        type="owner",
        subscription_status=OwnerSubscriptionStatus.FREE
    )
    db_session.add(owner_a)
    db_session.commit()

    # Propriedade A
    prop_a = Property(
        name="Fazenda A",
        property_type=PropertyType.BEEF,
        area=150.0,
        owner_id=owner_a.id_user
    )
    db_session.add(prop_a)
    db_session.commit()

    # Animal A
    animal_a = AnimalModel(
        identification_number=5001,
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

    # Pesagem A
    weigh_a = Weighing(
        weight=350.5,
        weigh_date=date.today(),
        animal_id=animal_a.id_animal
    )
    db_session.add(weigh_a)

    # Registro de Saúde A
    health_a = HealthModel(
        health_type=HealthType.VACCINE,
        product_name="Aftosa Premium",
        application_date=date.today(),
        property_id=prop_a.id_property,
        animal_id=animal_a.id_animal
    )
    db_session.add(health_a)
    db_session.commit()

    # Proprietário B (para teste de cross-tenant)
    owner_b = Owner(
        name="Owner B",
        email="owner_b@example.com",
        password="password_hash",
        cpf="444.444.444-44",
        type="owner",
        subscription_status=OwnerSubscriptionStatus.FREE
    )
    db_session.add(owner_b)
    db_session.commit()

    return {
        "token_a": create_access_token(owner_a.email, "owner"),
        "token_b": create_access_token(owner_b.email, "owner"),
        "prop_a": prop_a,
    }


def test_get_dashboard_anonymous_denied(client, dashboard_test_data):
    prop_id = dashboard_test_data["prop_a"].id_property
    response = client.get(f"/properties/{prop_id}/dashboard")
    assert response.status_code == 401


def test_get_dashboard_authorized_success(client, dashboard_test_data):
    token = dashboard_test_data["token_a"]
    prop_id = dashboard_test_data["prop_a"].id_property
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get(f"/properties/{prop_id}/dashboard", headers=headers)
    assert response.status_code == 200
    data = response.json()

    assert data["property_id"] == prop_id
    assert data["property_name"] == "Fazenda A"
    assert data["total_animals"] == 1
    assert len(data["recent_weighings"]) == 1
    assert data["recent_weighings"][0]["weight"] == 350.5
    assert data["recent_weighings"][0]["animal_identification"] == 5001
    assert len(data["recent_health_records"]) == 1
    assert data["recent_health_records"][0]["product_name"] == "Aftosa Premium"


def test_get_dashboard_cross_tenant_denied(client, dashboard_test_data):
    token_b = dashboard_test_data["token_b"]
    prop_id = dashboard_test_data["prop_a"].id_property
    headers = {"Authorization": f"Bearer {token_b}"}

    response = client.get(f"/properties/{prop_id}/dashboard", headers=headers)
    assert response.status_code == 404
