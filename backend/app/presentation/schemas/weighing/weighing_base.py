from typing import Optional
from pydantic import BaseModel, Field
from datetime import date

from app.presentation.schemas.common import BRDate

class WeighingBaseSchema(BaseModel):
    # 1. Primeiro os campos obrigatórios (sem valor padrão)
    weight: float = Field(..., example=450.5, description="Peso em kg")
    animal_id: int = Field(..., description="ID do animal vinculado")
    
    # 2. Depois o campo com valor padrão (e permitindo Optional para o PUT funcionar)
    weigh_date: Optional[BRDate] = Field(
        default_factory=date.today, description="Weighing date"
    )








































