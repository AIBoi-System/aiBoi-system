"""Cria usuário de teste para login no app até a home.

Uso (API rodando, ex.: docker compose up):
  cd backend
  python scripts/seed_test_user.py

Credenciais:
  E-mail: teste@aiboi.dev
  Senha:  Teste123!
"""

from __future__ import annotations

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy.orm import Session

from app.shared.infrastructure.database.connection import SessionLocal
from app.shared.infrastructure.persistence.user_repository import get_user_by_email
from app.shared.infrastructure.auth.security import hash_password
from app.shared.infrastructure.persistence.user import User

TEST_EMAIL = "teste@aiboi.dev"
TEST_PASSWORD = "Teste123!"
TEST_NAME = "Usuário Teste"
TEST_CPF = "52998224725"
TEST_PHONE = "11999999999"


def seed(db: Session) -> None:
    existing = get_user_by_email(db, TEST_EMAIL)
    if existing:
        existing.password = hash_password(TEST_PASSWORD)
        existing.name = TEST_NAME
        db.commit()
        print(f"Usuário já existia; senha atualizada: {TEST_EMAIL}")
        return

    user = User(
        name=TEST_NAME,
        email=TEST_EMAIL,
        phone=TEST_PHONE,
        cpf=TEST_CPF,
        password=hash_password(TEST_PASSWORD),
        type="user",
    )
    db.add(user)
    db.commit()
    print(f"Usuário criado: {TEST_EMAIL}")


def main() -> None:
    if os.getenv("ENV", "development").lower() == "production":
        raise RuntimeError("Seed de teste bloqueado em produção")
    if os.getenv("ALLOW_TEST_SEED", "false").lower() != "true":
        raise RuntimeError("Defina ALLOW_TEST_SEED=true para executar este seed")

    db = SessionLocal()
    try:
        seed(db)
        print("Seed de teste concluído")
    finally:
        db.close()


if __name__ == "__main__":
    main()
