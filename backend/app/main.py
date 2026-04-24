from fastapi import FastAPI
from app.core.database import (
    engine,
    Base,
)  # Importamos o Base para gerenciar as tabelas
from sqlalchemy import text


from app.models.animal import Animal
from app.models.reproduction import Reproduction
from app.models.health import Health
from app.models.weighing import Weighing
from app.models.batch import Batch
from app.models.user import User  #
from app.models.address import Address
from app.models.pasture import Pasture
from app.models.paddock import PaddockeStatus
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
from app.models.paddock import Paddock

app = FastAPI()

# =================================================================
# CRIAÇÃO AUTOMÁTICA DE TABELAS
# =================================================================
# Este comando percorre todos os modelos importados que herdam de Base
# e cria as tabelas no RDS se elas ainda não existirem.
try:
    Base.metadata.create_all(bind=engine)
    print("Mapeamento concluído: Tabelas criadas ou verificadas no RDS! 🚀")
except Exception as e:
    print(f"Erro ao mapear tabelas: {e}")


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
                "message": "Ligação ao RDS AWS estabelecida e tabelas prontas! 🚀",
            }
    except Exception as e:
        return {"status": "erro", "details": str(e)}
