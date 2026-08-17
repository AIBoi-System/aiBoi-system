from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.shared.infrastructure.database.connection import get_db
from app.modules.inventory.application.weighing_service import WeighingService
from app.presentation.schemas.weighing import (
    WeighingCreateSchema, 
    WeighingResponseSchema, 
    WeighingUpdateSchema
)
from app.presentation.api.auth_dependencies import get_current_user, verify_property_access

router = APIRouter(prefix="/weighings", tags=["Weighings"])


@router.post("/", response_model=WeighingResponseSchema, status_code=status.HTTP_201_CREATED)
def create(
    payload: WeighingCreateSchema,
    property_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    verify_property_access(db, property_id, current_user)
    return WeighingService.create_weighing(db, payload, property_id)


@router.get("/animal/{animal_id}", response_model=List[WeighingResponseSchema])
def get_by_animal(
    animal_id: int,
    property_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    verify_property_access(db, property_id, current_user)
    return WeighingService.get_history_by_animal(db, animal_id, property_id)


@router.put("/{id}", response_model=WeighingResponseSchema)
def update(
    id: int,
    property_id: int,
    payload: WeighingUpdateSchema,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    verify_property_access(db, property_id, current_user)
    return WeighingService.update_weighing(db, id, property_id, payload)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_weighing(
    id: int,
    property_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    verify_property_access(db, property_id, current_user)
    WeighingService.delete_weighing(db, id, property_id)
    return None















































