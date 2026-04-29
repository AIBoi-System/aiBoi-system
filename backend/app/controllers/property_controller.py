from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import (
    get_db,
)  # Certifique-se de ter essa função no seu database.py
from app.schemas.property_schema import (
    PropertyCreateSchema,
    PropertyUpdateSchema,
    PropertyResponseSchema,
)
from app.services.property_service import PropertyService

router = APIRouter(prefix="/properties", tags=["Propriedades"])


@router.post(
    "/", response_model=PropertyResponseSchema, status_code=status.HTTP_201_CREATED
)
def create_property(request: PropertyCreateSchema, db: Session = Depends(get_db)):
    return PropertyService.create_property(db, request)


@router.get("/", response_model=List[PropertyResponseSchema])
def list_properties(db: Session = Depends(get_db)):
    return PropertyService.get_all_properties(db)


@router.get("/{property_id}", response_model=PropertyResponseSchema)
def get_property(property_id: int, db: Session = Depends(get_db)):
    return PropertyService.get_property(db, property_id)


@router.put("/{property_id}", response_model=PropertyResponseSchema)
def update_property(
    property_id: int, request: PropertyUpdateSchema, db: Session = Depends(get_db)
):
    return PropertyService.update_property(db, property_id, request)


@router.delete("/{property_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_property(property_id: int, db: Session = Depends(get_db)):
    PropertyService.delete_property(db, property_id)
    return None
