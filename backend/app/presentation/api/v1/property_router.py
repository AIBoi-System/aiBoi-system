from app.presentation.api.auth_dependencies import get_current_user
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.shared.infrastructure.database.connection import (
    get_db,
)  # Certifique-se de ter essa função no seu database.py
from app.presentation.schemas.property_schema import (
    PropertyCreateSchema,
    PropertyUpdateSchema,
    PropertyResponseSchema,
)
from app.shared.application.property.property_service import PropertyService

router = APIRouter(prefix="/properties", tags=["Propriedades"])


@router.post(
    "/", response_model=PropertyResponseSchema, status_code=status.HTTP_201_CREATED
)
def create_property(
    request: PropertyCreateSchema,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # Garante que o owner_id da propriedade seja o usuário logado se não for admin
    if request.owner_id != current_user.id_user and current_user.type != "admin":
         request.owner_id = current_user.id_user

    return PropertyService.create_property(db, request)


@router.get("/", response_model=List[PropertyResponseSchema])
def list_properties(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return PropertyService.get_all_properties(db, owner_id=current_user.id_user)


@router.get("/{property_id}", response_model=PropertyResponseSchema)
def get_property(
    property_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return PropertyService.get_property_by_id(db, property_id, owner_id=current_user.id_user)


@router.put("/{property_id}", response_model=PropertyResponseSchema)
def update_property(
    property_id: int, request: PropertyUpdateSchema, db: Session = Depends(get_db)
):
    return PropertyService.update_property(db, property_id, request)


@router.delete("/{property_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_property(property_id: int, db: Session = Depends(get_db)):
    PropertyService.delete_property(db, property_id)
    return None
















































