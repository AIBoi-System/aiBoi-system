from fastapi import FastAPI
from app.core.database import engine, Base
from sqlalchemy import text

# IMPORTANTE: Importe todos os seus modelos aqui para que o SQLAlchemy os mapeie
from app.models.animal import Animal
from app.models.health import Health
from app.models.batch import Batch
from app.models.weighing import Weighing
from app.models.reproduction import Reproduction
from app.models.animal_event import AnimalEvent 

app = FastAPI()

# Este comando cria as tabelas no RDS se elas ainda não existirem
try:
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas ou verificadas com sucesso! 🚀")
except Exception as e:
    print(f"Erro ao criar tabelas: {e}")

@app.get("/")
def read_root():
    return {"status": "Online", "projeto": "AiBoi"}

@app.get("/test-db")
def test_db_connection():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            return {"status": "sucesso", "message": "Conexão e tabelas prontas no RDS!"}
    except Exception as e:
        return {"status": "erro", "details": str(e)}