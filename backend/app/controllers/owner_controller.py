from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from core.database import get_db
from schemas.owner.owner_create import OwnerCreateSchema
from schemas.owner.owner_update import OwnerUpdateSchema
from schemas.owner.owner_response import OwnerResponseSchema
from services.owner_service import (
    create_owner_service,
    get_owner_service,
    list_owners_service,
    update_owner_service,
    delete_owner_service,
)

router = APIRouter(
    prefix="/owners",
    tags=["Owners"]
)


@router.post(
    "",
    response_model=OwnerResponseSchema,
    status_code=status.HTTP_201_CREATED
)
def create_owner(
    owner_data: OwnerCreateSchema,
    db: Session = Depends(get_db)
):
    return create_owner_service(db, owner_data)


@router.get(
    "",
    response_model=List[OwnerResponseSchema],
    status_code=status.HTTP_200_OK
)
def list_owners(db: Session = Depends(get_db)):
    return list_owners_service(db)


@router.get(
    "/{id_user}",
    response_model=OwnerResponseSchema,
    status_code=status.HTTP_200_OK
)
def get_owner(
    id_user: int,
    db: Session = Depends(get_db)
):
    return get_owner_service(db, id_user)


@router.put(
    "/{id_user}",
    response_model=OwnerResponseSchema,
    status_code=status.HTTP_200_OK
)
def update_owner(
    id_user: int,
    owner_data: OwnerUpdateSchema,
    db: Session = Depends(get_db)
):
    return update_owner_service(db, id_user, owner_data)


@router.delete(
    "/{id_user}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_owner(
    id_user: int,
    db: Session = Depends(get_db)
):
    delete_owner_service(db, id_user)
    return None