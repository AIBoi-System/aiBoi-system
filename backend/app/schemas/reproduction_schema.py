from typing import Optional
from pydantic import BaseModel, Field
from app.enums.reproduction.reproduction_type import ReproductionType
from app.enums.step.step_status import StepStatus


class ProtocolStartRequest(BaseModel):
    """
    Schema que define o formato exato do JSON que o celular do
    pecuarista vai enviar para iniciar um protocolo de reprodução.
    """

    animal_id: int = Field(
        ..., description="ID da vaca que vai iniciar o protocolo", example=1
    )
    protocol_type: ReproductionType = Field(
        ..., description="Tipo do protocolo (IATF, FIV, etc.)"
    )


class ProtocolResponse(BaseModel):
    """
    Schema que define a resposta que a nossa API vai devolver
    para o celular em caso de sucesso.
    """

    message: str
    animal_id: int
    protocol: str
    status: str


class StepUpdateRequest(BaseModel):
    """Schema para atualizar o status de uma etapa específica."""

    status: StepStatus = Field(
        ..., description="O novo status da etapa (ex: COMPLETED)"
    )
    notes: Optional[str] = Field(
        None, description="Alguma observação do pecuarista (opcional)"
    )
