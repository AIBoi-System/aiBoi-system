from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.modules.inventory.application.reproduction_service import ReproductionService
from app.shared.infrastructure.database.connection import get_db
from app.presentation.api.auth_dependencies import (
    get_current_user,
    require_roles,
    verify_property_access,
)
from app.presentation.schemas.reproduction_schema import (
    BirthRecordRequest,
    ProtocolCreate,
    ProtocolResponse,
    ReproductionCreate,
    ReproductionResponse,
    ReproductionUpdate,
    StepCreate,
    StepExecutionCreate,
    StepExecutionResponse,
    StepResponse,
)

router = APIRouter(prefix="/reproductions", tags=["Reprodução"])


@router.post(
    "/protocols",
    response_model=ProtocolResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles("admin"))],
)
def create_protocol(payload: ProtocolCreate, db: Session = Depends(get_db)):
    return ReproductionService.create_protocol(db, payload)


@router.get(
    "/protocols",
    response_model=List[ProtocolResponse],
    dependencies=[Depends(require_roles("user", "owner", "admin"))],
)
def list_protocols(db: Session = Depends(get_db)):
    return ReproductionService.list_protocols(db)


@router.get(
    "/protocols/{protocol_id}",
    response_model=ProtocolResponse,
    dependencies=[Depends(require_roles("user", "owner", "admin"))],
)
def get_protocol(protocol_id: int, db: Session = Depends(get_db)):
    return ReproductionService.get_protocol(db, protocol_id)


@router.post(
    "/protocols/{protocol_id}/steps",
    response_model=StepResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles("admin"))],
)
def create_step(protocol_id: int, payload: StepCreate, db: Session = Depends(get_db)):
    return ReproductionService.create_step(db, protocol_id, payload)


@router.get(
    "/protocols/{protocol_id}/steps",
    response_model=List[StepResponse],
    dependencies=[Depends(require_roles("user", "owner", "admin"))],
)
def list_steps(protocol_id: int, db: Session = Depends(get_db)):
    return ReproductionService.list_steps_by_protocol(db, protocol_id)


@router.post(
    "/",
    response_model=ReproductionResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles("owner", "admin"))],
)
def create_reproduction(
    property_id: int,
    payload: ReproductionCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    verify_property_access(db, property_id, current_user)
    return ReproductionService.create_reproduction(db, payload, current_user, property_id)


@router.get(
    "/",
    response_model=List[ReproductionResponse],
    dependencies=[Depends(require_roles("user", "owner", "admin"))],
)
def list_reproductions(
    property_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    verify_property_access(db, property_id, current_user)
    return ReproductionService.list_reproductions(db, property_id)


@router.get(
    "/{reproduction_id}",
    response_model=ReproductionResponse,
    dependencies=[Depends(require_roles("user", "owner", "admin"))],
)
def get_reproduction(
    reproduction_id: int,
    property_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    verify_property_access(db, property_id, current_user)
    return ReproductionService.get_reproduction(db, reproduction_id, property_id)


@router.put(
    "/{reproduction_id}",
    response_model=ReproductionResponse,
    dependencies=[Depends(require_roles("owner", "admin"))],
)
def update_reproduction(
    reproduction_id: int,
    property_id: int,
    payload: ReproductionUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    verify_property_access(db, property_id, current_user)
    return ReproductionService.update_reproduction(db, reproduction_id, property_id, payload)


@router.delete(
    "/{reproduction_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_roles("owner", "admin"))],
)
def delete_reproduction(
    reproduction_id: int,
    property_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    verify_property_access(db, property_id, current_user)
    ReproductionService.delete_reproduction(db, reproduction_id, property_id)
    return None


@router.post(
    "/{reproduction_id}/executions",
    response_model=StepExecutionResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles("owner", "admin"))],
)
def create_step_execution(
    reproduction_id: int,
    property_id: int,
    payload: StepExecutionCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    verify_property_access(db, property_id, current_user)
    return ReproductionService.create_step_execution(db, reproduction_id, property_id, payload)


@router.get(
    "/{reproduction_id}/executions",
    response_model=List[StepExecutionResponse],
    dependencies=[Depends(require_roles("user", "owner", "admin"))],
)
def list_step_executions(
    reproduction_id: int,
    property_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    verify_property_access(db, property_id, current_user)
    return ReproductionService.list_executions_by_reproduction(db, reproduction_id, property_id)


@router.post(
    "/{reproduction_id}/birth",
    response_model=ReproductionResponse,
    dependencies=[Depends(require_roles("owner", "admin"))],
)
def register_birth(
    reproduction_id: int,
    property_id: int,
    payload: BirthRecordRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    verify_property_access(db, property_id, current_user)
    return ReproductionService.register_birth(db, reproduction_id, property_id, payload)















































