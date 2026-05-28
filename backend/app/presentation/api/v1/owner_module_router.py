from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.application.owner_module.service import OwnerModuleService
from app.infrastructure.database.connection import get_db
from app.presentation.api.auth_dependencies import require_roles
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
    dependencies=[Depends(require_roles("owner", "admin"))],
)
def list_modules(owner_id: int, db: Session = Depends(get_db)):
    return OwnerModuleService.list_owner_modules(db, owner_id)
