from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.shared.infrastructure.database.connection import get_db
from app.presentation.schemas.pasture_schema import PastureCreate, PastureUpdate, PastureResponse
from app.modules.inventory.application.pasture_service import pasture_service
from app.presentation.api.auth_dependencies import get_current_user, verify_property_access

router = APIRouter(prefix="/pastures", tags=["Pastures"])


@router.post("/", response_model=PastureResponse, status_code=status.HTTP_201_CREATED)
def create_pasture(
    pasture: PastureCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    verify_property_access(db, pasture.property_id, current_user)
    return pasture_service.create_pasture(db, pasture)


@router.get("/", response_model=List[PastureResponse])
def get_pastures(
    property_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    verify_property_access(db, property_id, current_user)
    return pasture_service.get_pastures(
        db, skip=skip, limit=limit, property_id=property_id
    )


@router.get("/{pasture_id}", response_model=PastureResponse)
def get_pasture(
    pasture_id: int,
    property_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    verify_property_access(db, property_id, current_user)
    return pasture_service.get_pasture(db, pasture_id, property_id)


@router.put("/{pasture_id}", response_model=PastureResponse)
def update_pasture(
    pasture_id: int,
    property_id: int,
    pasture_update: PastureUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    verify_property_access(db, property_id, current_user)
    if pasture_update.property_id is not None and pasture_update.property_id != property_id:
        verify_property_access(db, pasture_update.property_id, current_user)
    return pasture_service.update_pasture(db, pasture_id, property_id, pasture_update)


@router.delete("/{pasture_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pasture(
    pasture_id: int,
    property_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    verify_property_access(db, property_id, current_user)
    pasture_service.delete_pasture(db, pasture_id, property_id)
    return None















































