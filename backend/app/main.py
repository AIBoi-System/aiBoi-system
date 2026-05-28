import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

raw_origins = os.getenv("CORS_ALLOWED_ORIGINS", "*")
allowed_origins = [origin.strip() for origin in raw_origins.split(",") if origin.strip()]

register_exception_handlers(app)
app.include_router(api_v1_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def security_headers_middleware(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    if request.url.path.startswith("/docs") or request.url.path.startswith("/redoc"):
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "img-src 'self' data: https://fastapi.tiangolo.com"
        )
    else:
        response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response


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
