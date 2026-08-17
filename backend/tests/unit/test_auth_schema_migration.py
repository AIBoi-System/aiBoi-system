import os

from alembic import command
from alembic.config import Config
from alembic.migration import MigrationContext
from alembic.autogenerate import compare_metadata
from sqlalchemy import create_engine, inspect, text

from app.infrastructure.persistence import models  # noqa: F401
from app.shared.infrastructure.database.connection import Base


INITIAL_REVISION = "fdae6f06aeb9"
HEAD_REVISION = "7b9d2c4e6f81"


def _alembic_config() -> Config:
    return Config("alembic.ini")


def test_auth_schema_upgrade_copies_cpf_and_downgrade_restores_it(
    tmp_path,
    monkeypatch,
):
    database_path = tmp_path / "auth-schema.sqlite3"
    database_url = f"sqlite:///{database_path.as_posix()}"
    monkeypatch.setenv("MIGRATION_DATABASE_URL", database_url)
    monkeypatch.setenv("DATABASE_URL", database_url)
    config = _alembic_config()

    command.upgrade(config, INITIAL_REVISION)
    engine = create_engine(database_url)
    with engine.begin() as connection:
        connection.execute(
            text(
                "INSERT INTO users "
                "(id_user, name, email, password, cpf, type) "
                "VALUES (1, 'Pessoa Teste', 'migration@example.com', "
                "'hash', '529.982.247-25', 'user')"
            )
        )
    engine.dispose()

    command.upgrade(config, "head")
    engine = create_engine(database_url)
    inspector = inspect(engine)
    assert "cpf" not in {column["name"] for column in inspector.get_columns("users")}
    assert {"cpfs", "phone_verification_codes", "auth_sessions"}.issubset(
        inspector.get_table_names()
    )
    with engine.connect() as connection:
        assert connection.execute(
            text("SELECT user_id, number FROM cpfs")
        ).one() == (1, "529.982.247-25")
        drift = compare_metadata(MigrationContext.configure(connection), Base.metadata)
    assert drift == []
    engine.dispose()

    command.downgrade(config, INITIAL_REVISION)
    engine = create_engine(database_url)
    inspector = inspect(engine)
    assert "cpf" in {column["name"] for column in inspector.get_columns("users")}
    assert not {"cpfs", "phone_verification_codes", "auth_sessions"}.intersection(
        inspector.get_table_names()
    )
    with engine.connect() as connection:
        assert connection.execute(
            text("SELECT cpf FROM users WHERE id_user = 1")
        ).scalar_one() == "529.982.247-25"
        assert connection.execute(
            text("SELECT version_num FROM alembic_version")
        ).scalar_one() == INITIAL_REVISION
    engine.dispose()


def test_migration_revision_contract():
    assert HEAD_REVISION == "7b9d2c4e6f81"
    assert os.path.exists("alembic/versions/7b9d2c4e6f81_auth_identity_sessions.py")
