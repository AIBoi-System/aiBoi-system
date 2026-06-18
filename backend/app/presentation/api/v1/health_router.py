from typing import List

from fastapi import APIRouter, Depends

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

router = APIRouter(prefix="/health", tags=["Health"])


def _schema_to_entity(schema: HealthCreate) -> HealthRecord:
    return HealthRecord(**schema.model_dump())


@router.post("/", response_model=HealthResponse)
def create_health(
    payload: HealthCreate,
    use_case: CreateHealthRecordUseCase = Depends(get_create_health_use_case),
):
    created = use_case.execute(_schema_to_entity(payload))
    return HealthResponse.model_validate(created)


@router.get("/", response_model=List[HealthResponse])
def list_health(
    use_case: ListHealthRecordsUseCase = Depends(get_list_health_use_case),
):
    records = use_case.execute()
    return [HealthResponse.model_validate(r) for r in records]


@router.get("/{health_id}", response_model=HealthResponse)
def get_health(
    health_id: int,
    use_case: GetHealthRecordUseCase = Depends(get_get_health_use_case),
):
    record = use_case.execute(health_id)
    return HealthResponse.model_validate(record)


@router.put("/{health_id}", response_model=HealthResponse)
def update_health(
    health_id: int,
    payload: HealthUpdate,
    use_case: UpdateHealthRecordUseCase = Depends(get_update_health_use_case),
):
    updated = use_case.execute(health_id, payload.model_dump(exclude_unset=True))
    return HealthResponse.model_validate(updated)


@router.delete("/{health_id}")
def delete_health(
    health_id: int,
    use_case: DeleteHealthRecordUseCase = Depends(get_delete_health_use_case),
):
    use_case.execute(health_id)
    return {"message": "Registro de saúde deletado com sucesso."}














































