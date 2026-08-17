import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["ENV"] = "test"

from app.shared.infrastructure.database.connection import Base, get_db
from app.infrastructure.persistence import models  # noqa: F401
from app.main import app

TEST_ENGINE = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=TEST_ENGINE)


@pytest.fixture(scope="session", autouse=True)
def create_tables():
    Base.metadata.create_all(bind=TEST_ENGINE)
    yield
    Base.metadata.drop_all(bind=TEST_ENGINE)


@pytest.fixture
def db_session():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(autouse=True)
def clean_database(db_session):
    yield
    for table in reversed(Base.metadata.sorted_tables):
        db_session.execute(table.delete())
    db_session.commit()


@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def auth_setup(db_session):
    from app.shared.infrastructure.persistence.owner import Owner
    from app.shared.infrastructure.persistence.property import Property
    from app.enums.property.property_type import PropertyType
    from app.enums.owner.owner_subscription_status import OwnerSubscriptionStatus
    from app.shared.infrastructure.auth.auth import create_access_token

    owner = Owner(
        name="Test Owner",
        email="test_owner@example.com",
        password="hash_password",
        cpf="999.999.999-99",
        type="owner",
        subscription_status=OwnerSubscriptionStatus.FREE
    )
    db_session.add(owner)
    db_session.commit()
    db_session.refresh(owner)

    property_ = Property(
        name="Fazenda Teste",
        property_type=PropertyType.BEEF,
        area=120.0,
        owner_id=owner.id_user
    )
    db_session.add(property_)
    db_session.commit()
    db_session.refresh(property_)

    token = create_access_token(owner.email, "owner")

    return {
        "owner": owner,
        "property": property_,
        "token": token,
        "headers": {"Authorization": f"Bearer {token}"}
    }

