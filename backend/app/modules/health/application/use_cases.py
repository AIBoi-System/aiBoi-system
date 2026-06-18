from typing import List

from app.modules.health.domain.entity import HealthRecord
from app.modules.health.domain.repository import HealthRepository
from app.shared.domain.exceptions import DomainException, EntityNotFoundError


class CreateHealthRecordUseCase:
    def __init__(self, repository: HealthRepository):
        self._repository = repository

    def execute(self, record: HealthRecord) -> HealthRecord:
        record.validate_target()
        return self._repository.save(record)


class ListHealthRecordsUseCase:
    def __init__(self, repository: HealthRepository):
        self._repository = repository

    def execute(self) -> List[HealthRecord]:
        return self._repository.list_all()


class GetHealthRecordUseCase:
    def __init__(self, repository: HealthRepository):
        self._repository = repository

    def execute(self, health_id: int) -> HealthRecord:
        record = self._repository.get_by_id(health_id)
        if not record:
            raise EntityNotFoundError("Registro de saúde", health_id)
        return record


class UpdateHealthRecordUseCase:
    def __init__(self, repository: HealthRepository):
        self._repository = repository

    def execute(self, health_id: int, data: dict) -> HealthRecord:
        record = self._repository.update(health_id, data)
        if not record:
            raise EntityNotFoundError("Registro de saúde", health_id)
        return record


class DeleteHealthRecordUseCase:
    def __init__(self, repository: HealthRepository):
        self._repository = repository

    def execute(self, health_id: int) -> None:
        if not self._repository.delete(health_id):
            raise EntityNotFoundError("Registro de saúde", health_id)














