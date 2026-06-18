from abc import ABC, abstractmethod
from typing import List, Optional

from app.modules.health.domain.entity import HealthRecord


class HealthRepository(ABC):
    @abstractmethod
    def get_by_id(self, health_id: int) -> Optional[HealthRecord]:
        pass

    @abstractmethod
    def list_all(self) -> List[HealthRecord]:
        pass

    @abstractmethod
    def save(self, record: HealthRecord) -> HealthRecord:
        pass

    @abstractmethod
    def update(self, health_id: int, data: dict) -> Optional[HealthRecord]:
        pass

    @abstractmethod
    def delete(self, health_id: int) -> bool:
        pass









































