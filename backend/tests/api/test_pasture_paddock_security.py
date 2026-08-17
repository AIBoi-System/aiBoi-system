import pytest
from app.shared.infrastructure.auth.auth import create_access_token
from app.shared.infrastructure.persistence.owner import Owner
from app.shared.infrastructure.persistence.property import Property
from app.shared.infrastructure.persistence.pasture import Pasture
from app.shared.infrastructure.persistence.paddock import Paddock
from app.enums.property.property_type import PropertyType
from app.enums.pasture.pasture_management import PastureManagement
from app.enums.paddock.paddocke_status import PaddockeStatus
from app.enums.owner.owner_subscription_status import OwnerSubscriptionStatus

@pytest.fixture
def test_users_and_properties(db_session):
    # Criar Proprietário A
    owner_a = Owner(
        name="User A",
        email="user_a@example.com",
        password="hash_password",
        cpf="111.111.111-11",
        type="owner",
        subscription_status=OwnerSubscriptionStatus.FREE
    )
    db_session.add(owner_a)
    db_session.commit()

    # Criar Propriedade do Usuário A
    prop_a = Property(
        name="Fazenda A",
        property_type=PropertyType.BEEF,
        area=100.0,
        owner_id=owner_a.id_user
    )
    db_session.add(prop_a)
    db_session.commit()

    # Criar Proprietário B
    owner_b = Owner(
        name="User B",
        email="user_b@example.com",
        password="hash_password",
        cpf="222.222.222-22",
        type="owner",
        subscription_status=OwnerSubscriptionStatus.FREE
    )
    db_session.add(owner_b)
    db_session.commit()

    # Criar Propriedade do Usuário B
    prop_b = Property(
        name="Fazenda B",
        property_type=PropertyType.BEEF,
        area=200.0,
        owner_id=owner_b.id_user
    )
    db_session.add(prop_b)
    db_session.commit()

    return {
        "user_a": owner_a,
        "token_a": create_access_token(owner_a.email, "owner"),
        "prop_a": prop_a,
        "user_b": owner_b,
        "token_b": create_access_token(owner_b.email, "owner"),
        "prop_b": prop_b,
    }


def test_anonymous_access_denied(client):
    # Pastures
    assert client.get("/pastures/").status_code == 401
    assert client.post("/pastures/", json={}).status_code == 401
    assert client.get("/pastures/1").status_code == 401
    assert client.put("/pastures/1", json={}).status_code == 401
    assert client.delete("/pastures/1").status_code == 401

    # Paddocks
    assert client.get("/paddocks/").status_code == 401
    assert client.post("/paddocks/", json={}).status_code == 401
    assert client.get("/paddocks/1").status_code == 401
    assert client.put("/paddocks/1", json={}).status_code == 401
    assert client.delete("/paddocks/1").status_code == 401


def test_authorized_owner_crud_pasture(client, test_users_and_properties):
    token = test_users_and_properties["token_a"]
    prop_id = test_users_and_properties["prop_a"].id_property
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Criar pastagem
    payload = {
        "name": "Pasto Verde",
        "area": 10.5,
        "capacity": 50,
        "grazing_management": PastureManagement.ROTATIONAL.value,
        "property_id": prop_id,
        "notes": "Pasto fértil"
    }
    create_resp = client.post("/pastures/", json=payload, headers=headers)
    assert create_resp.status_code == 201
    pasture_id = create_resp.json()["id_pasture"]

    # 2. Listar pastagens da propriedade
    list_resp = client.get(f"/pastures/?property_id={prop_id}", headers=headers)
    assert list_resp.status_code == 200
    assert len(list_resp.json()) == 1
    assert list_resp.json()[0]["id_pasture"] == pasture_id

    # 3. Obter pastagem individual
    get_resp = client.get(
        f"/pastures/{pasture_id}?property_id={prop_id}", headers=headers
    )
    assert get_resp.status_code == 200
    assert get_resp.json()["name"] == "Pasto Verde"

    # 4. Atualizar pastagem
    update_resp = client.put(
        f"/pastures/{pasture_id}?property_id={prop_id}",
        json={"name": "Pasto Novo"},
        headers=headers,
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["name"] == "Pasto Novo"

    # 5. Deletar pastagem
    delete_resp = client.delete(
        f"/pastures/{pasture_id}?property_id={prop_id}", headers=headers
    )
    assert delete_resp.status_code == 204


def test_cross_tenant_pasture_denied(client, test_users_and_properties, db_session):
    # Criar uma pastagem pertencente ao Usuário A
    prop_a = test_users_and_properties["prop_a"]
    
    pasture_a = Pasture(
        name="Pasto do A",
        area=15.0,
        capacity=30,
        grazing_management=PastureManagement.ROTATIONAL,
        property_id=prop_a.id_property
    )
    db_session.add(pasture_a)
    db_session.commit()

    # Usuário B tenta interagir com a pastagem do Usuário A usando seu token_b
    token_b = test_users_and_properties["token_b"]
    headers_b = {"Authorization": f"Bearer {token_b}"}

    # Listar as pastagens da propriedade A passando token de B -> deve falhar com 404
    list_resp = client.get(f"/pastures/?property_id={prop_a.id_property}", headers=headers_b)
    assert list_resp.status_code == 404

    # Buscar pastagem individual do A usando token de B -> deve retornar 404
    get_resp = client.get(
        f"/pastures/{pasture_a.id_pasture}?property_id={prop_a.id_property}",
        headers=headers_b,
    )
    assert get_resp.status_code == 404

    # Atualizar pastagem do A usando token de B -> deve retornar 404
    update_resp = client.put(
        f"/pastures/{pasture_a.id_pasture}?property_id={prop_a.id_property}",
        json={"name": "Invasão"},
        headers=headers_b,
    )
    assert update_resp.status_code == 404

    # Deletar pastagem do A usando token de B -> deve retornar 404
    delete_resp = client.delete(
        f"/pastures/{pasture_a.id_pasture}?property_id={prop_a.id_property}",
        headers=headers_b,
    )
    assert delete_resp.status_code == 404


def test_authorized_owner_crud_paddock(client, test_users_and_properties):
    token = test_users_and_properties["token_a"]
    prop_id = test_users_and_properties["prop_a"].id_property
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Criar piquete
    payload = {
        "name": "Piquete Alpha",
        "area_ha": 5.0,
        "grass_type": "Brachiaria",
        "forage_quality": "BOA",
        "animal_capacity": 20,
        "paddock_status": PaddockeStatus.AVAILABLE.value,
        "property_id": prop_id,
        "notes": "Piquete inicial"
    }
    create_resp = client.post("/paddocks/", json=payload, headers=headers)
    assert create_resp.status_code == 201
    paddock_id = create_resp.json()["id_paddock"]

    # 2. Listar piquetes da propriedade
    list_resp = client.get(f"/paddocks/?property_id={prop_id}", headers=headers)
    assert list_resp.status_code == 200
    assert len(list_resp.json()) == 1
    assert list_resp.json()[0]["id_paddock"] == paddock_id

    # 3. Obter piquete individual
    get_resp = client.get(
        f"/paddocks/{paddock_id}?property_id={prop_id}", headers=headers
    )
    assert get_resp.status_code == 200
    assert get_resp.json()["name"] == "Piquete Alpha"

    # 4. Atualizar piquete
    update_resp = client.put(
        f"/paddocks/{paddock_id}?property_id={prop_id}",
        json={"name": "Piquete Beta"},
        headers=headers,
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["name"] == "Piquete Beta"

    # 5. Deletar piquete
    delete_resp = client.delete(
        f"/paddocks/{paddock_id}?property_id={prop_id}", headers=headers
    )
    assert delete_resp.status_code == 204


def test_cross_tenant_paddock_denied(client, test_users_and_properties, db_session):
    # Criar um piquete pertencente ao Usuário A
    prop_a = test_users_and_properties["prop_a"]
    
    paddock_a = Paddock(
        name="Piquete do A",
        area_ha=4.0,
        grass_type="Tifton",
        forage_quality="EXCELENTE",
        animal_capacity=15,
        paddock_status=PaddockeStatus.AVAILABLE,
        property_id=prop_a.id_property
    )
    db_session.add(paddock_a)
    db_session.commit()

    # Usuário B tenta interagir com o piquete do Usuário A usando seu token_b
    token_b = test_users_and_properties["token_b"]
    headers_b = {"Authorization": f"Bearer {token_b}"}

    # Listar piquetes da propriedade A passando token de B -> deve falhar com 404
    list_resp = client.get(f"/paddocks/?property_id={prop_a.id_property}", headers=headers_b)
    assert list_resp.status_code == 404

    # Buscar piquete individual do A usando token de B -> deve retornar 404
    get_resp = client.get(
        f"/paddocks/{paddock_a.id_paddock}?property_id={prop_a.id_property}",
        headers=headers_b,
    )
    assert get_resp.status_code == 404

    # Atualizar piquete do A usando token de B -> deve retornar 404
    update_resp = client.put(
        f"/paddocks/{paddock_a.id_paddock}?property_id={prop_a.id_property}",
        json={"name": "Invasão"},
        headers=headers_b,
    )
    assert update_resp.status_code == 404

    # Deletar piquete do A usando token de B -> deve retornar 404
    delete_resp = client.delete(
        f"/paddocks/{paddock_a.id_paddock}?property_id={prop_a.id_property}",
        headers=headers_b,
    )
    assert delete_resp.status_code == 404
