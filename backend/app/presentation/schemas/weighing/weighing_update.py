from pydantic import BaseModel
from typing import Optional

from app.presentation.schemas.common import BRDate


class WeighingUpdateSchema(BaseModel):
    weight: Optional[float] = None
    weigh_date: Optional[BRDate] = None
    class Config:
        from_attributes = True
