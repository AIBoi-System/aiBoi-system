from app.shared.infrastructure.database.connection import (
    _normalize_database_url,
    _override_database_host,
)


def test_normalizes_supabase_postgres_url_for_psycopg() -> None:
    assert (
        _normalize_database_url("postgres://user:password@host:5432/postgres")
        == "postgresql+psycopg://user:password@host:5432/postgres"
    )


def test_normalizes_standard_postgresql_url_for_psycopg() -> None:
    assert (
        _normalize_database_url("postgresql://user:password@host:5432/postgres")
        == "postgresql+psycopg://user:password@host:5432/postgres"
    )


def test_preserves_explicit_sqlalchemy_driver() -> None:
    url = "postgresql+psycopg://user:password@host:5432/postgres"
    assert _normalize_database_url(url) == url


def test_preserves_sqlite_test_url() -> None:
    assert _normalize_database_url("sqlite:///:memory:") == "sqlite:///:memory:"


def test_overrides_postgres_host_for_container_runtime() -> None:
    url = "postgresql+psycopg://user:password@localhost:5432/db_agrofence"

    assert _override_database_host(url, "host.docker.internal") == (
        "postgresql+psycopg://user:password@host.docker.internal:5432/db_agrofence"
    )


def test_keeps_url_when_host_override_is_not_configured() -> None:
    url = "postgresql+psycopg://user:password@localhost:5432/db_agrofence"

    assert _override_database_host(url, None) == url
