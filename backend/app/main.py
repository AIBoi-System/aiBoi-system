from fastapi import FastAPI
from sqlalchemy import text

from app.infrastructure.database.connection import Base, engine
from app.infrastructure.persistence import models  # noqa: F401 — registra tabelas
from app.presentation.api.exception_handlers import register_exception_handlers
from app.presentation.api.v1.router import api_v1_router

app = FastAPI(
    title="AiBoi API",
    version="2.0.0",
    description="Gestão bovina — Clean Architecture + DDD",
)

register_exception_handlers(app)
app.include_router(api_v1_router)


try:
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas/verificadas com sucesso!")
except Exception as e:
    print(f"Erro ao criar tabelas: {e}")


@app.get("/")
def read_root():
    return {"status": "Online", "projeto": "AiBoi", "arquitetura": "Clean + DDD"}


@app.get("/test-db")
def test_db_connection():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            return {
                "status": "sucesso",
                "message": "Conexão com banco OK",
            }
    except Exception as e:
        return {"status": "erro", "details": str(e)}
