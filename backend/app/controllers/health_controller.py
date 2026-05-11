from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db

from app.schemas.health.health_create import HealthCreate
from app.schemas.health.health_update import HealthUpdate
from app.schemas.health.health_response import HealthResponse
from app.services.health_service import HealthService

from app.schemas.health_schema import HealthRecordRequest, HealthRecordResponse
from app.services.health_service import create_health_record_service


router = APIRouter(prefix="/health", tags=["Health"])


@router.post("/", response_model=HealthResponse)
def create_health(data: HealthCreate, db: Session = Depends(get_db)):
    return HealthService.create(db, data)


@router.get("/", response_model=List[HealthResponse])
def get_all_health(db: Session = Depends(get_db)):
    return HealthService.get_all(db)


@router.get("/{health_id}", response_model=HealthResponse)
def get_health_by_id(health_id: int, db: Session = Depends(get_db)):
    return HealthService.get_by_id(db, health_id)


@router.put("/{health_id}", response_model=HealthResponse)
def update_health(
    health_id: int,
    data: HealthUpdate,
    db: Session = Depends(get_db)
):
    return HealthService.update(db, health_id, data)


@router.delete("/{health_id}")
def delete_health(health_id: int, db: Session = Depends(get_db)):
    return HealthService.delete(db, health_id)


@router.post("/record", response_model=HealthRecordResponse, status_code=201)
def create_health_record(request: HealthRecordRequest, db: Session = Depends(get_db)):
    try:
        health_record = create_health_record_service(db, request)

        alvo = (
            f"Animal {request.animal_id}"
            if request.animal_id
            else f"Lote {request.batch_id}"
        )

        return HealthRecordResponse(
            message=f"Registro de {request.health_type.value} ({request.product_name}) salvo com sucesso!",
            target=alvo,
        )

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao registrar saúde: {str(e)}"
        )