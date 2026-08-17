from typing import List
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.modules.health.application.use_cases import (
    CreateHealthRecordUseCase,
    DeleteHealthRecordUseCase,
    GetHealthRecordUseCase,
    ListHealthRecordsUseCase,
    UpdateHealthRecordUseCase,
)
from app.modules.health.domain.entity import HealthRecord
from app.presentation.api.dependencies import (
    get_create_health_use_case,
    get_delete_health_use_case,
    get_get_health_use_case,
    get_list_health_use_case,
    get_update_health_use_case,
)
from app.presentation.schemas.health.health_create import HealthCreate
from app.presentation.schemas.health.health_response import HealthResponse
from app.presentation.schemas.health.health_update import HealthUpdate
from app.presentation.api.v1.mappers import health_to_response

from app.presentation.api.auth_dependencies import get_current_user, verify_property_access
from app.shared.infrastructure.database.connection import get_db

router = APIRouter(prefix="/health", tags=["Health"])


def _schema_to_entity(schema: HealthCreate) -> HealthRecord:
    return HealthRecord(**schema.model_dump())


@router.post(
    "/", response_model=HealthResponse, status_code=status.HTTP_201_CREATED
)
def create_health(
    payload: HealthCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    use_case: CreateHealthRecordUseCase = Depends(get_create_health_use_case),
):
    verify_property_access(db, payload.property_id, current_user)
    created = use_case.execute(_schema_to_entity(payload))
    return health_to_response(created)


@router.get("/", response_model=List[HealthResponse])
def list_health(
    property_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    use_case: ListHealthRecordsUseCase = Depends(get_list_health_use_case),
):
    verify_property_access(db, property_id, current_user)
    records = use_case.execute(property_id)
    return [health_to_response(r) for r in records]


@router.get("/{health_id}", response_model=HealthResponse)
def get_health(
    health_id: int,
    property_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    use_case: GetHealthRecordUseCase = Depends(get_get_health_use_case),
):
    verify_property_access(db, property_id, current_user)
    record = use_case.execute(health_id, property_id)
    return health_to_response(record)


@router.put("/{health_id}", response_model=HealthResponse)
def update_health(
    health_id: int,
    property_id: int,
    payload: HealthUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    use_case: UpdateHealthRecordUseCase = Depends(get_update_health_use_case),
):
    verify_property_access(db, property_id, current_user)
    if payload.property_id is not None and payload.property_id != property_id:
        verify_property_access(db, payload.property_id, current_user)

    updated = use_case.execute(health_id, property_id, payload.model_dump(exclude_unset=True))
    return health_to_response(updated)


@router.delete("/{health_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_health(
    health_id: int,
    property_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    use_case: DeleteHealthRecordUseCase = Depends(get_delete_health_use_case),
):
    verify_property_access(db, property_id, current_user)
    use_case.execute(health_id, property_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)














































