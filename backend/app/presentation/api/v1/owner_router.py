from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.shared.infrastructure.database.connection import get_db
from app.presentation.schemas.owner.owner_create import OwnerCreateSchema, OwnerResponseSchema
from app.presentation.schemas.owner.owner_update import OwnerUpdateSchema
import app.shared.application.user.owner_service as owner_service
from app.presentation.api.auth_dependencies import get_current_user

router = APIRouter(prefix="/owners", tags=["Owners"])


@router.post(
    "", response_model=OwnerResponseSchema, status_code=status.HTTP_201_CREATED
)
def create_owner(
    owner_data: OwnerCreateSchema,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if current_user.type != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso não autorizado.")
    return owner_service.create_owner_service(db, owner_data)


# Upgrade de User para Owner
@router.post(
    "/{id_user}/upgrade",
    response_model=OwnerResponseSchema,
    status_code=status.HTTP_200_OK,
)
def upgrade_to_owner(
    id_user: int,
    subscription_status: str = "FREE",
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Transforma um usuário comum já existente em um Dono (Owner).
    """
    if current_user.type != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso não autorizado.")
    owner = owner_service.upgrade_user_to_owner_service(db, id_user, subscription_status)
    if not owner:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado ou erro ao realizar upgrade.",
        )
    return owner


@router.get(
    "", response_model=List[OwnerResponseSchema], status_code=status.HTTP_200_OK
)
def list_owners(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if current_user.type != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso não autorizado.")
    return owner_service.list_owners_service(db)


@router.get(
    "/{id_user}", response_model=OwnerResponseSchema, status_code=status.HTTP_200_OK
)
def get_owner(
    id_user: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if current_user.type != "admin" and (current_user.id_user != id_user or current_user.type != "owner"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso não autorizado.")
    return owner_service.get_owner_service(db, id_user)


@router.put(
    "/{id_user}", response_model=OwnerResponseSchema, status_code=status.HTTP_200_OK
)
def update_owner(
    id_user: int,
    owner_data: OwnerUpdateSchema,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if current_user.type != "admin" and (current_user.id_user != id_user or current_user.type != "owner"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso não autorizado.")
    return owner_service.update_owner_service(db, id_user, owner_data)


@router.delete("/{id_user}", status_code=status.HTTP_204_NO_CONTENT)
def delete_owner(
    id_user: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if current_user.type != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso não autorizado.")
    owner_service.delete_owner_service(db, id_user)
    return None















































