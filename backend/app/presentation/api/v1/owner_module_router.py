from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.shared.application.user.owner_module_service import OwnerModuleService
from app.shared.infrastructure.database.connection import get_db
from app.presentation.api.auth_dependencies import require_roles, get_current_user
from app.presentation.schemas.owner_module_schema import (
    OwnerModuleCreate,
    OwnerModuleResponse,
)

router = APIRouter(prefix="/owner-modules", tags=["Owner Modules"])


@router.post(
    "/",
    response_model=OwnerModuleResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles("admin"))],
)
def assign_module(payload: OwnerModuleCreate, db: Session = Depends(get_db)):
    return OwnerModuleService.assign_module(db, payload)


@router.get(
    "/{owner_id}",
    response_model=List[OwnerModuleResponse],
)
def list_modules(
    owner_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if current_user.type != "admin" and (current_user.id_user != owner_id or current_user.type != "owner"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso não autorizado.")
    return OwnerModuleService.list_owner_modules(db, owner_id)














































