import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Localiza a raiz do projeto (subindo 4 níveis a partir de backend/app/core/)
# Caminho esperado: aiBoi-system/.env
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
env_path = BASE_DIR / ".env"

# 2. Carrega o .env explicitamente do caminho encontrado
load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL")

# 3. Validação para evitar erros de conexão vazia
if not DATABASE_URL:
    raise ValueError(
        f"ERRO: DATABASE_URL não encontrada. Verifique o arquivo .env em: {env_path}"
    )

# 4. Configuração do Engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Importante para manter a conexão ativa com o RDS da AWS
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# cria uma fabrica de sessões ligada ao engine que temos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# injeçao de dependencia do fastapi
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
