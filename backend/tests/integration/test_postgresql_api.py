"""Opt-in API smoke test against the migrated local PostgreSQL database.

All writes run inside an external transaction configured as rollback-only. Enable
with RUN_POSTGRES_INTEGRATION=1; credentials stay in POSTGRES_TEST_DATABASE_URL
or backend/.env and are never printed by this test.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from uuid import uuid4

import pytest
from dotenv import dotenv_values
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select, text
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session

from app.enums.owner.owner_subscription_status import OwnerSubscriptionStatus
from app.enums.property.property_type import PropertyType
from app.enums.animal.animal_category import AnimalCategory
from app.enums.animal.animal_life_status import AnimalLifeStatus
from app.enums.animal.animal_origin import AnimalOrigin
from app.enums.animal.animal_reproductive_status import AnimalReproductiveStatus
from app.enums.animal.animal_sex import AnimalSex
from app.enums.animal.animal_size import AnimalSize
from app.main import app
from app.presentation.api.auth_dependencies import get_current_user
from app.shared.infrastructure.auth.auth import create_access_token
from app.shared.infrastructure.database.connection import get_db
from app.shared.infrastructure.persistence.owner import Owner
from app.shared.infrastructure.persistence.property import Property
from app.shared.infrastructure.persistence.user import User


pytestmark = pytest.mark.postgresql

LOCAL_HOSTS = {"localhost", "127.0.0.1", "::1"}
EXPECTED_DATABASE = "db_agrofence"


@dataclass(repr=False)
class PostgreSQLAPIContext:
    client: TestClient
    headers: dict[str, str]
    other_headers: dict[str, str]
    property_id: int
    other_property_id: int
    marker: str

    def __repr__(self) -> str:
        return "PostgreSQLAPIContext(credentials=<redacted>)"


def _local_postgresql_url() -> str:
    if os.getenv("RUN_POSTGRES_INTEGRATION") != "1":
        pytest.skip("set RUN_POSTGRES_INTEGRATION=1 to run local PostgreSQL tests")

    database_url = os.getenv("POSTGRES_TEST_DATABASE_URL")
    if not database_url:
        env_values = dotenv_values(Path(__file__).resolve().parents[2] / ".env")
        database_url = env_values.get("DATABASE_URL")
    if not database_url:
        pytest.skip("local PostgreSQL test URL is not configured")

    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql+psycopg://", 1)
    elif database_url.startswith("postgresql://"):
        database_url = database_url.replace(
            "postgresql://", "postgresql+psycopg://", 1
        )

    parsed = make_url(database_url)
    if (
        parsed.drivername != "postgresql+psycopg"
        or parsed.host not in LOCAL_HOSTS
        or parsed.database != EXPECTED_DATABASE
    ):
        pytest.fail(
            "PostgreSQL integration tests only accept the local db_agrofence database",
            pytrace=False,
        )
    return database_url


@pytest.fixture
def postgresql_api_client():
    database_url = _local_postgresql_url()
    engine = create_engine(
        database_url,
        pool_pre_ping=True,
        connect_args={
            "connect_timeout": 5,
            "application_name": "agrofence-transactional-api-test",
        },
    )
    marker = uuid4().hex
    owner_email = f"codex-pg-{marker}@example.invalid"

    connection = engine.connect()
    transaction = connection.begin()
    session = Session(
        bind=connection,
        expire_on_commit=False,
        join_transaction_mode="rollback_only",
    )

    try:
        migration = session.execute(text("SELECT version_num FROM alembic_version"))
        assert migration.scalar_one_or_none()

        owner = Owner(
            name="PostgreSQL Transaction Test",
            email=owner_email,
            password="not-used-by-this-test",
            cpf=f"{int(marker[:11], 16) % 10**11:011d}",
            account_status="Ativo",
            type="owner",
            subscription_status=OwnerSubscriptionStatus.FREE,
        )
        session.add(owner)
        session.flush()

        property_ = Property(
            name="Fazenda Transacional",
            area=42.0,
            property_type=PropertyType.BEEF,
            owner_id=owner.id_user,
        )
        session.add(property_)
        session.flush()

        other_owner = Owner(
            name="PostgreSQL Other Tenant",
            email=f"codex-pg-other-{marker}@example.invalid",
            password="not-used-by-this-test",
            cpf=f"{(int(marker[11:22], 16) + 1) % 10**11:011d}",
            account_status="Ativo",
            type="owner",
            subscription_status=OwnerSubscriptionStatus.FREE,
        )
        session.add(other_owner)
        session.flush()
        other_property = Property(
            name="Fazenda Isolada",
            area=10.0,
            property_type=PropertyType.BEEF,
            owner_id=other_owner.id_user,
        )
        session.add(other_property)
        session.flush()

        def override_get_db():
            yield session

        app.dependency_overrides[get_db] = override_get_db
        with TestClient(app) as client:
            yield PostgreSQLAPIContext(
                client=client,
                headers={
                    "Authorization": f"Bearer {create_access_token(owner.email, 'owner')}"
                },
                other_headers={
                    "Authorization": f"Bearer {create_access_token(other_owner.email, 'owner')}"
                },
                property_id=property_.id_property,
                other_property_id=other_property.id_property,
                marker=marker,
            )
    finally:
        app.dependency_overrides.pop(get_db, None)
        app.dependency_overrides.pop(get_current_user, None)
        session.close()
        if transaction.is_active:
            transaction.rollback()
        connection.close()

        with engine.connect() as verification_connection:
            remaining = verification_connection.execute(
                select(User.id_user).where(User.email == owner_email)
            ).first()
            assert remaining is None, "external PostgreSQL transaction was not rolled back"
        engine.dispose()


def test_api_to_local_postgresql_cruds_are_transactional(postgresql_api_client):
    client = postgresql_api_client.client
    headers = postgresql_api_client.headers
    other_headers = postgresql_api_client.other_headers
    property_id = postgresql_api_client.property_id
    other_property_id = postgresql_api_client.other_property_id
    marker = postgresql_api_client.marker

    health_response = client.get("/test-db")
    assert health_response.status_code == 200
    assert health_response.json()["status"] == "sucesso"

    pasture_create = client.post(
        "/pastures/",
        headers=headers,
        json={
            "name": f"Pasto {marker[:8]}",
            "area": 8.5,
            "capacity": 30,
            "grazing_management": "Rotacionado",
            "property_id": property_id,
        },
    )
    assert pasture_create.status_code == 201, pasture_create.text
    pasture_id = pasture_create.json()["id_pasture"]
    assert client.get(
        f"/pastures/{pasture_id}?property_id={property_id}", headers=headers
    ).status_code == 200
    assert client.put(
        f"/pastures/{pasture_id}?property_id={property_id}",
        headers=headers,
        json={"capacity": 35},
    ).status_code == 200

    batch_create = client.post(
        "/batches/",
        headers=headers,
        json={
            "name": f"Lote {marker[:8]}",
            "batch_purpose": "Reproducao",
            "status": "ACTIVE",
            "category": "HEIFER",
            "check_in": date.today().isoformat(),
            "property_id": property_id,
        },
    )
    assert batch_create.status_code == 201, batch_create.text
    batch_id = batch_create.json()["id_batch"]
    assert client.get(
        f"/batches/{batch_id}?property_id={property_id}", headers=headers
    ).status_code == 200
    assert client.put(
        f"/batches/{batch_id}?property_id={property_id}",
        headers=headers,
        json={"status": "INACTIVE"},
    ).status_code == 200

    animal_create = client.post(
        f"/animals/?property_id={property_id}",
        headers=headers,
        json={
            "identification_number": int(marker[:8], 16) % 1_000_000_000,
            "sex": AnimalSex.F.value,
            "animal_size": AnimalSize.MEDIUM_SIZE.value,
            "animal_life_status": AnimalLifeStatus.ACTIVE.value,
            "reproductive_status": AnimalReproductiveStatus.OPEN.value,
            "animal_category": AnimalCategory.HEIFER.value,
            "birth_date": "2022-03-15",
            "origin": AnimalOrigin.BIRTH.value,
            "name": f"PG-{marker[:6]}",
        },
    )
    assert animal_create.status_code == 201, animal_create.text
    animal_id = animal_create.json()["id_animal"]

    assert client.get(
        f"/animals/{animal_id}?property_id={other_property_id}",
        headers=other_headers,
    ).status_code == 404

    health_create = client.post(
        "/health/",
        headers=headers,
        json={
            "health_type": "VACCINE",
            "product_name": "Vacina transacional",
            "application_date": date.today().isoformat(),
            "property_id": property_id,
            "animal_id": animal_id,
        },
    )
    assert health_create.status_code == 201, health_create.text
    health_id = health_create.json()["id_health_record"]
    assert client.get(
        f"/health/{health_id}?property_id={property_id}", headers=headers
    ).status_code == 200
    assert client.put(
        f"/health/{health_id}?property_id={property_id}",
        headers=headers,
        json={"notes": "validado no PostgreSQL"},
    ).status_code == 200

    weighing_create = client.post(
        f"/weighings/?property_id={property_id}",
        headers=headers,
        json={
            "animal_id": animal_id,
            "weight": 410.5,
            "weigh_date": date.today().isoformat(),
        },
    )
    assert weighing_create.status_code == 201, weighing_create.text
    weighing_id = weighing_create.json()["id"]
    assert client.get(
        f"/weighings/animal/{animal_id}?property_id={property_id}", headers=headers
    ).status_code == 200
    assert client.put(
        f"/weighings/{weighing_id}?property_id={property_id}",
        headers=headers,
        json={"weight": 415.0},
    ).status_code == 200

    reproduction_create = client.post(
        f"/reproductions/?property_id={property_id}",
        headers=headers,
        json={
            "reproduction_type": "Monta Natural",
            "reproduction_status": "In Progress",
            "start_date": date.today().isoformat(),
            "animal_id": animal_id,
        },
    )
    assert reproduction_create.status_code == 201, reproduction_create.text
    reproduction_id = reproduction_create.json()["id"]
    assert client.get(
        f"/reproductions/{reproduction_id}?property_id={property_id}",
        headers=headers,
    ).status_code == 200
    assert client.delete(
        f"/reproductions/{reproduction_id}?property_id={property_id}",
        headers=headers,
    ).status_code == 204

    assert client.delete(
        f"/weighings/{weighing_id}?property_id={property_id}", headers=headers
    ).status_code == 204
    assert client.delete(
        f"/health/{health_id}?property_id={property_id}", headers=headers
    ).status_code == 204
    assert client.delete(
        f"/animals/{animal_id}?property_id={property_id}", headers=headers
    ).status_code == 204
    assert client.delete(
        f"/batches/{batch_id}?property_id={property_id}", headers=headers
    ).status_code == 204
    assert client.delete(
        f"/pastures/{pasture_id}?property_id={property_id}", headers=headers
    ).status_code == 204
