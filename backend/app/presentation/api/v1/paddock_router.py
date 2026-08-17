from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.shared.infrastructure.database.connection import get_db
from app.presentation.schemas.paddock_schema import PaddockCreate, PaddockUpdate, PaddockResponse
from app.modules.inventory.application.paddock_service import paddock_service
from app.presentation.api.auth_dependencies import get_current_user, verify_property_access

router = APIRouter(prefix="/paddocks", tags=["Paddocks"])


@router.post("/", response_model=PaddockResponse, status_code=status.HTTP_201_CREATED)
def create_paddock(
    paddock: PaddockCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    verify_property_access(db, paddock.property_id, current_user)
    return paddock_service.create_paddock(db, paddock)


@router.get("/", response_model=List[PaddockResponse])
def get_paddocks(
    property_id: int,
    skip: int = 0,
    limit: int = 100,
    pasture_id: int = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    verify_property_access(db, property_id, current_user)
    return paddock_service.get_paddocks(
        db, skip=skip, limit=limit, property_id=property_id, pasture_id=pasture_id
    )


@router.get("/{paddock_id}", response_model=PaddockResponse)
def get_paddock(
    paddock_id: int,
    property_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    verify_property_access(db, property_id, current_user)
    return paddock_service.get_paddock(db, paddock_id, property_id)


@router.put("/{paddock_id}", response_model=PaddockResponse)
def update_paddock(
    paddock_id: int,
    property_id: int,
    paddock_update: PaddockUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    verify_property_access(db, property_id, current_user)
    if paddock_update.property_id is not None and paddock_update.property_id != property_id:
        verify_property_access(db, paddock_update.property_id, current_user)
    return paddock_service.update_paddock(db, paddock_id, property_id, paddock_update)


@router.delete("/{paddock_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_paddock(
    paddock_id: int,
    property_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    verify_property_access(db, property_id, current_user)
    paddock_service.delete_paddock(db, paddock_id, property_id)
    return None















































