from fastapi import FastAPI
from sqlalchemy import text
from app.core.database import engine, Base

# --- IMPORTAÇÃO DOS MODELOS ---
# Mantemos as importações explícitas para garantir a criação das tabelas
from app.models.animal import Animal
from app.models.reproduction import Reproduction
from app.models.health import Health
from app.models.weighing import Weighing
from app.models.batch import Batch
from app.models.user import User
from app.models.address import Address
from app.models.pasture import Pasture
from app.models.paddock import PaddockeStatus, Paddock
from app.models.owner import Owner
from app.models.cpf import CPF
from app.models.property import Property
from app.models.step import Step
from app.models.step_execution import StepExecution
from app.models.protocol import Protocol
from app.models.animal_movement import AnimalMovement
from app.models.batch_movement import BatchMovement
from app.models.animal_event import AnimalEvent
from app.models.death_record import DeathRecord

# --- IMPORTAÇÃO DOS CONTROLLERS (ROTAS) ---
from app.controllers import (
    user_controller,
    property_controller,
    reproduction_controller,
    health_controller,
)

# --- CRIAÇÃO DA APLICAÇÃO ---

app = FastAPI(title="AiBoi API", version="1.0.0")

# ================================
# REGISTRO DE ROTAS
# ================================
app.include_router(user_controller.router)
app.include_router(property_controller.router)
app.include_router(reproduction_controller.router)
app.include_router(health_controller.router)

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
