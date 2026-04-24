from pydantic import BaseModel, Field
from typing import Optional
from app.enums.health.health_type import HealthType


class HealthRecordRequest(BaseModel):
    """Schema para receber os dados de uma vacina ou tratamento."""

    health_type: HealthType = Field(
        ..., description="Tipo do registro (VACCINE, MEDICATION, etc)"
    )
    product_name: str = Field(..., description="Nome do produto aplicado")
    dosage: float = Field(..., description="Dose aplicada")

    # Opcionais, pois pode ser para um animal OU para um lote
    animal_id: Optional[int] = Field(
        None, description="ID do animal (se for individual)"
    )
    batch_id: Optional[int] = Field(None, description="ID do lote (se for em massa)")


class HealthRecordResponse(BaseModel):
    """Schema para a resposta de sucesso."""

    message: str
    target: str
