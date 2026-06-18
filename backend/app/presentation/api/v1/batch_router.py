from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.modules.inventory.application.batch_service import BatchService
from app.shared.infrastructure.database.connection import get_db
from app.presentation.schemas.batch_schema import (
    BatchCreate,
    BatchResponse,
    BatchUpdate,
)

router = APIRouter(prefix="/batches", tags=["Batch"])


@router.post(
    "/",
    response_model=BatchResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_batch(payload: BatchCreate, db: Session = Depends(get_db)):
    return BatchService.create_batch(db, payload)


@router.get("/", response_model=List[BatchResponse])
def list_batches(db: Session = Depends(get_db)):
    return BatchService.list_batches(db)


@router.get("/{batch_id}", response_model=BatchResponse)
def get_batch(batch_id: int, db: Session = Depends(get_db)):
    return BatchService.get_batch(db, batch_id)


@router.put("/{batch_id}", response_model=BatchResponse)
def update_batch(batch_id: int, payload: BatchUpdate, db: Session = Depends(get_db)):
    return BatchService.update_batch(db, batch_id, payload)


@router.delete("/{batch_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_batch(batch_id: int, db: Session = Depends(get_db)):
    BatchService.delete_batch(db, batch_id)
    return None














































