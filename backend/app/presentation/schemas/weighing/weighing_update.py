from pydantic import BaseModel
from datetime import date
from typing import Optional

class WeighingUpdateSchema(BaseModel):
    weight: Optional[float] = None
    weigh_date: Optional[date] = None
    class Config:
        from_attributes = True
