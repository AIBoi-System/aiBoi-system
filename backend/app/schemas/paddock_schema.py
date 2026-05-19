from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from app.enums.paddock.paddocke_status import PaddockeStatus


# base
class PaddockBase(BaseModel):
    name: str = Field(..., max_length=100, description="Nome ou número do piquete")
    area_ha: float = Field(..., gt=0, description="Área do piquete em hectares")
    grass_type: Optional[str] = Field(
        None, max_length=100, description="Tipo de capim (ex: Brachiaria)"
    )
    forage_quality: Optional[str] = Field(
        None, max_length=100, description="Qualidade da forragem"
    )
    animal_capacity: int = Field(
        ..., ge=0, description="Quantas cabeças o piquete suporta"
    )
    paddock_status: PaddockeStatus
    notes: Optional[str] = None
    property_id: int
    pasture_id: Optional[int] = (
        None  # é opcional caso o piquete ainda nao tenha sido alocado num pasto
    )


# create
class PaddockCreate(PaddockBase):
    pass


# update
class PaddockUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    area_ha: Optional[float] = Field(None, gt=0)
    grass_type: Optional[str] = Field(None, max_length=100)
    forage_quality: Optional[str] = Field(None, max_length=100)
    animal_capacity: Optional[int] = Field(None, ge=0)
    paddock_status: Optional[PaddockeStatus] = None
    notes: Optional[str] = None
    property_id: Optional[int] = None
    pasture_id: Optional[int] = None


# response
class PaddockResponse(PaddockBase):
    id_paddock: int

    model_config = ConfigDict(from_attributes=True)
