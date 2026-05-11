from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db

from app.schemas.health.health_create import HealthCreate
from app.schemas.health.health_update import HealthUpdate
from app.schemas.health.health_response import HealthResponse
from app.services.health_service import HealthService


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


