import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine, make_url
from sqlalchemy.orm import declarative_base, sessionmaker

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path)

raw_database_url = os.getenv("DATABASE_URL")

if not raw_database_url:
    raise ValueError(
        f"ERRO: DATABASE_URL não encontrada. Verifique o arquivo .env em: {env_path}"
    )


def _normalize_database_url(database_url: str) -> str:
    """Normaliza URLs PostgreSQL para psycopg 3 e rejeita drivers legados."""
    if database_url.startswith("postgres://"):
        return database_url.replace("postgres://", "postgresql+psycopg://", 1)
    if database_url.startswith("postgresql://"):
        return database_url.replace("postgresql://", "postgresql+psycopg://", 1)
    if database_url.startswith(("postgresql+psycopg://", "sqlite://")):
        return database_url
    raise ValueError(
        "DATABASE_URL deve usar PostgreSQL com psycopg 3 "
        "(postgresql+psycopg://). SQLite e permitido apenas nos testes."
    )


def _override_database_host(database_url: str, host: str | None) -> str:
    """Aplica host alternativo para processos executados em contêineres."""
    if not host or not database_url.startswith("postgresql+psycopg://"):
        return database_url

    return make_url(database_url).set(host=host).render_as_string(
        hide_password=False
    )


DATABASE_URL = _override_database_host(
    _normalize_database_url(raw_database_url),
    os.getenv("DATABASE_HOST_OVERRIDE"),
)


def _create_engine(database_url: str) -> Engine:
    options: dict[str, object] = {"pool_pre_ping": True}
    if database_url.startswith("postgresql+psycopg://"):
        options.update(
            pool_size=int(os.getenv("DB_POOL_SIZE", "5")),
            max_overflow=int(os.getenv("DB_MAX_OVERFLOW", "5")),
            pool_timeout=int(os.getenv("DB_POOL_TIMEOUT", "30")),
            pool_recycle=int(os.getenv("DB_POOL_RECYCLE", "1800")),
            pool_use_lifo=True,
            connect_args={
                "connect_timeout": int(os.getenv("DB_CONNECT_TIMEOUT", "10")),
                "application_name": os.getenv("DB_APPLICATION_NAME", "agrofence-api"),
            },
        )
    return create_engine(database_url, **options)


engine = _create_engine(DATABASE_URL)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    # expire_on_commit=False prevents DetachedInstanceError when accessing 
    # model attributes after the transaction is committed (common in FastAPI route returns).
    expire_on_commit=False,
    bind=engine,
)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
