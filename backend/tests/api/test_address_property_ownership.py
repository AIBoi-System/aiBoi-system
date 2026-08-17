import pytest
from types import SimpleNamespace

from app.main import app
from app.presentation.api.auth_dependencies import get_current_user
from app.enums.owner.owner_subscription_status import OwnerSubscriptionStatus
from app.enums.property.property_type import PropertyType
from app.shared.infrastructure.auth.auth import create_access_token
from app.shared.infrastructure.persistence.address import Address
from app.shared.infrastructure.persistence.owner import Owner
from app.shared.infrastructure.persistence.property import Property


@pytest.fixture
def address_tenants(db_session):
    address_a = Address(
        zip_code="01001-000",
        state="SP",
        neighborhood="Centro",
        street_name="Rua A",
        number="10",
    )
    address_b = Address(
        zip_code="20040-020",
        state="RJ",
        neighborhood="Centro",
        street_name="Rua B",
        number="20",
    )
    db_session.add_all([address_a, address_b])
    db_session.flush()

    owner_a = Owner(
        name="Address Owner A",
        email="address_owner_a@example.com",
        password="hash_password",
        cpf="333.333.333-33",
        type="owner",
        address_id=address_a.id_address,
        subscription_status=OwnerSubscriptionStatus.FREE,
    )
    owner_b = Owner(
        name="Address Owner B",
        email="address_owner_b@example.com",
        password="hash_password",
        cpf="444.444.444-44",
        type="owner",
        address_id=address_b.id_address,
        subscription_status=OwnerSubscriptionStatus.FREE,
    )
    db_session.add_all([owner_a, owner_b])
    db_session.flush()

    property_a = Property(
        name="Property A",
        property_type=PropertyType.BEEF,
        area=100.0,
        owner_id=owner_a.id_user,
        address_id=address_a.id_address,
    )
    property_b = Property(
        name="Property B",
        property_type=PropertyType.BEEF,
        area=100.0,
        owner_id=owner_b.id_user,
        address_id=address_b.id_address,
    )
    db_session.add_all([property_a, property_b])
    db_session.commit()

    def headers(user):
        token = create_access_token(user.email, user.type)
        return {"Authorization": f"Bearer {token}"}

    return {
        "address_a": address_a,
        "address_b": address_b,
        "owner_a": owner_a,
        "owner_b": owner_b,
        "property_a": property_a,
        "property_b": property_b,
        "headers_a": headers(owner_a),
        "headers_b": headers(owner_b),
    }


def use_admin_identity():
    app.dependency_overrides[get_current_user] = lambda: SimpleNamespace(
        id_user=999_999, type="admin"
    )


def test_address_get_and_update_are_owner_scoped(client, address_tenants):
    address_a = address_tenants["address_a"]

    own_get = client.get(
        f"/addresses/{address_a.id_address}",
        headers=address_tenants["headers_a"],
    )
    assert own_get.status_code == 200

    cross_get = client.get(
        f"/addresses/{address_a.id_address}",
        headers=address_tenants["headers_b"],
    )
    assert cross_get.status_code == 404

    cross_update = client.put(
        f"/addresses/{address_a.id_address}",
        json={"street_name": "Cross tenant"},
        headers=address_tenants["headers_b"],
    )
    assert cross_update.status_code == 404

    use_admin_identity()
    admin_get = client.get(f"/addresses/{address_a.id_address}")
    assert admin_get.status_code == 200


def test_owner_cannot_transfer_property_or_claim_foreign_address(
    client, db_session, address_tenants
):
    property_a = address_tenants["property_a"]
    owner_b = address_tenants["owner_b"]
    address_b = address_tenants["address_b"]

    owner_transfer = client.put(
        f"/properties/{property_a.id_property}",
        json={"owner_id": owner_b.id_user},
        headers=address_tenants["headers_a"],
    )
    assert owner_transfer.status_code == 400

    address_transfer = client.put(
        f"/properties/{property_a.id_property}",
        json={"address_id": address_b.id_address},
        headers=address_tenants["headers_a"],
    )
    assert address_transfer.status_code == 404

    db_session.refresh(property_a)
    assert property_a.owner_id == address_tenants["owner_a"].id_user
    assert property_a.address_id == address_tenants["address_a"].id_address


def test_admin_transfer_requires_address_compatible_with_target_owner(
    client, db_session, address_tenants
):
    property_a = address_tenants["property_a"]
    owner_b = address_tenants["owner_b"]

    use_admin_identity()
    incompatible = client.put(
        f"/properties/{property_a.id_property}",
        json={"owner_id": owner_b.id_user},
    )
    assert incompatible.status_code == 404

    compatible = client.put(
        f"/properties/{property_a.id_property}",
        json={
            "owner_id": owner_b.id_user,
            "address_id": address_tenants["address_b"].id_address,
        },
    )
    assert compatible.status_code == 200

    db_session.refresh(property_a)
    assert property_a.owner_id == owner_b.id_user
    assert property_a.address_id == address_tenants["address_b"].id_address
