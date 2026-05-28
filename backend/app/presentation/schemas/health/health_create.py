from pydantic import BaseModel
from typing import Optional

from app.domain.enums.health.health_type import HealthType
from app.presentation.schemas.common import BRDate


class HealthCreate(BaseModel):
    health_type: HealthType
    product_name: str
    application_date: BRDate
    responsible: Optional[str] = None
    dosage: Optional[float] = None
    unit_price: Optional[float] = None
    notes: Optional[str] = None
    animal_id: Optional[int] = None
    batch_id: Optional[int] = None