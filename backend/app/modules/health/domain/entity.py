from dataclasses import dataclass
from datetime import date
from typing import Optional

from app.enums.health.health_type import HealthType
from app.shared.domain.entity import Entity
from app.shared.domain.exceptions import DomainException


@dataclass(kw_only=True)
class HealthRecord(Entity):
    health_type: HealthType
    product_name: str
    application_date: date
    responsible: Optional[str] = None
    dosage: Optional[float] = None
    unit_price: Optional[float] = None
    notes: Optional[str] = None
    animal_id: Optional[int] = None
    batch_id: Optional[int] = None

    def validate_target(self) -> None:
        if not self.animal_id and not self.batch_id:
            raise DomainException("Informe animal_id ou batch_id.")
        if self.animal_id and self.batch_id:
            raise DomainException("Informe apenas animal_id OU batch_id, não ambos.")









































