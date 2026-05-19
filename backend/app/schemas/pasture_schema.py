from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from app.enums.pasture.pasture_management import PastureManagement


# base
class PastureBase(BaseModel):
    name: str = Field(..., max_length=100, description="Nome de identificação do pasto")
    area: float = Field(..., gt=0, description="Área total do pasto (em hectares)")
    capacity: int = Field(..., ge=0, description="Capacidade máxima de animais")
    grazing_management: PastureManagement
    notes: Optional[str] = None
    property_id: int


# create
class PastureCreate(PastureBase):
    pass


# update
class PastureUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    area: Optional[float] = Field(None, gt=0)
    capacity: Optional[int] = Field(None, ge=0)
    grazing_management: Optional[PastureManagement] = None
    notes: Optional[str] = None
    property_id: Optional[int] = None


# response
class PastureResponse(PastureBase):
    id_pasture: int

    # le os dados que vem do SQLAlchemy
    model_config = ConfigDict(from_attributes=True)
