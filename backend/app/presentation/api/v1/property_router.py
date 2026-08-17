from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.presentation.api.auth_dependencies import get_current_user
from app.presentation.schemas.dashboard_schema import DashboardResponseSchema
from app.presentation.schemas.property_schema import (
    PropertyCreateSchema,
    PropertyResponseSchema,
    PropertyUpdateSchema,
)
from app.shared.application.property.property_service import PropertyService
from app.shared.infrastructure.database.connection import get_db

router = APIRouter(prefix="/properties", tags=["Propriedades"])


def _is_admin(current_user) -> bool:
    return (current_user.type or "").casefold() == "admin"


@router.post(
    "/", response_model=PropertyResponseSchema, status_code=status.HTTP_201_CREATED
)
def create_property(
    request: PropertyCreateSchema,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return PropertyService.create_property(
        db,
        request,
        actor_id=current_user.id_user,
        is_admin=_is_admin(current_user),
    )


@router.get("/", response_model=List[PropertyResponseSchema])
def list_properties(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return PropertyService.get_all_properties(
        db,
        owner_id=None if _is_admin(current_user) else current_user.id_user,
    )


@router.get("/{property_id}", response_model=PropertyResponseSchema)
def get_property(
    property_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return PropertyService.get_property_by_id(
        db,
        property_id,
        owner_id=None if _is_admin(current_user) else current_user.id_user,
    )


@router.put("/{property_id}", response_model=PropertyResponseSchema)
def update_property(
    property_id: int,
    request: PropertyUpdateSchema,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return PropertyService.update_property(
        db,
        property_id,
        request,
        actor_id=current_user.id_user,
        is_admin=_is_admin(current_user),
    )


@router.delete("/{property_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_property(
    property_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    PropertyService.delete_property(
        db,
        property_id,
        actor_id=current_user.id_user,
        is_admin=_is_admin(current_user),
    )
    return None


@router.get("/{property_id}/dashboard", response_model=DashboardResponseSchema)
def get_property_dashboard(
    property_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return PropertyService.get_dashboard(
        db,
        property_id,
        actor_id=current_user.id_user,
        is_admin=_is_admin(current_user),
    )
