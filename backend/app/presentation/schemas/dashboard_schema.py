from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class RecentWeighingSchema(BaseModel):
    id: int
    weight: float
    weigh_date: date
    animal_id: int
    animal_identification: int

class RecentHealthSchema(BaseModel):
    id_health_record: int
    health_type: str
    product_name: str
    application_date: date
    responsible: Optional[str] = None
    animal_id: Optional[int] = None

class DashboardResponseSchema(BaseModel):
    property_id: int
    property_name: str
    total_animals: int
    total_pastures: int
    total_paddocks: int
    total_batches: int
    recent_weighings: List[RecentWeighingSchema]
    recent_health_records: List[RecentHealthSchema]
