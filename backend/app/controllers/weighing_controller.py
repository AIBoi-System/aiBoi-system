from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.services.weighing_service import WeighingService
from app.schemas.weighing import (
    WeighingCreateSchema, 
    WeighingResponseSchema, 
    WeighingUpdateSchema
)
router = APIRouter(prefix="/weighings", tags=["Weighings"])

@router.post("/", response_model=WeighingResponseSchema, status_code=status.HTTP_201_CREATED)
def create(payload: WeighingCreateSchema, db: Session = Depends(get_db)):
    return WeighingService.create_weighing(db, payload)

@router.get("/animal/{animal_id}", response_model=List[WeighingResponseSchema])
def get_by_animal(animal_id: int, db: Session = Depends(get_db)):
    return WeighingService.get_history_by_animal(db, animal_id)

@router.put("/{id}", response_model=WeighingResponseSchema)
def update(id: int, payload: WeighingUpdateSchema, db: Session = Depends(get_db)):
    return WeighingService.update_weighing(db, id, payload)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_weighing(id: int, db: Session = Depends(get_db)):
    WeighingService.delete_weighing(db, id)
    return None
