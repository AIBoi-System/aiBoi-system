from fastapi import FastAPI
from app.core.database import engine
from sqlalchemy import text

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "Online", "projeto": "AiBoi"}

@app.get("/test-db")
def test_db_connection():
    try:
        # Tenta executar uma consulta simples no MySQL
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            return {"status": "sucesso", "message": "Ligação ao RDS AWS estabelecida! 🚀"}
    except Exception as e:
        return {"status": "erro", "details": str(e)}