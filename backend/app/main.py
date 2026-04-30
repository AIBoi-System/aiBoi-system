from fastapi import FastAPI
from sqlalchemy import text

from app.core.database import engine, Base


from app.models import *

# controllers
from app.controllers import (
    user_controller,
    reproduction_controller,
    health_controller,
    owner_controller
)

app = FastAPI(
    title="AiBoi API",
    version="1.0.0"
)

# ================================
# REGISTRO DE ROTAS
# ================================
app.include_router(user_controller.router)
app.include_router(reproduction_controller.router)
app.include_router(health_controller.router)
app.include_router(owner_controller.router)
# ================================
# CRIAÇÃO DE TABELAS
# ================================
try:
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas/verificadas com sucesso!")
except Exception as e:
    print(f"Erro ao criar tabelas: {e}")

# ================================
# ROTAS BASE
# ================================
@app.get("/")
def read_root():
    return {"status": "Online", "projeto": "AiBoi"}


@app.get("/test-db")
def test_db_connection():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            return {
                "status": "sucesso",
                "message": "Conexão com banco OK 🚀",
            }
    except Exception as e:
        return {"status": "erro", "details": str(e)}