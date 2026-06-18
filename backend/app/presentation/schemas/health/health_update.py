from pydantic import BaseModel
from typing import Optional

from app.enums.health.health_type import HealthType
from app.presentation.schemas.common import BRDate


class HealthUpdate(BaseModel):
    health_type: Optional[HealthType] = None
    product_name: Optional[str] = None
    application_date: Optional[BRDate] = None
    responsible: Optional[str] = None
    dosage: Optional[float] = None
    unit_price: Optional[float] = None
    notes: Optional[str] = None
    animal_id: Optional[int] = None
    batch_id: Optional[int] = None








































