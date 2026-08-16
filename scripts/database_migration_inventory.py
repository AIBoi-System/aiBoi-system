"""Inventário seguro das conexões PostgreSQL de runtime e migration.

Não imprime URLs, credenciais ou conteúdo das tabelas.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import make_url


ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / "backend" / ".env")


def _inventory(variable: str) -> dict[str, object]:
    raw_url = os.getenv(variable)
    if not raw_url:
        return {"configured": False}

    if raw_url.startswith("postgres://"):
        raw_url = raw_url.replace("postgres://", "postgresql+psycopg://", 1)
    elif raw_url.startswith("postgresql://"):
        raw_url = raw_url.replace("postgresql://", "postgresql+psycopg://", 1)

    url = make_url(raw_url)
    if url.drivername != "postgresql+psycopg":
        raise RuntimeError(f"{variable} deve apontar para PostgreSQL com psycopg 3")

    engine = create_engine(raw_url, pool_pre_ping=True, connect_args={"connect_timeout": 10})
    try:
        with engine.connect() as connection:
            inspector = inspect(connection)
            tables = inspector.get_table_names()
            counts = {
                table: connection.execute(
                    text(f'SELECT count(*) FROM "{table}"')
                ).scalar_one()
                for table in tables
            }
            version = connection.execute(text("SELECT version()")).scalar_one()
        return {
            "configured": True,
            "backend": url.get_backend_name(),
            "server_version": str(version),
            "table_count": len(tables),
            "row_counts": counts,
        }
    finally:
        engine.dispose()


def main() -> None:
    print(
        json.dumps(
            {
                "source": _inventory("DATABASE_URL"),
                "destination": _inventory("MIGRATION_DATABASE_URL"),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
