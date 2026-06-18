from pydantic import BaseModel, Field
from typing import Optional
from app.enums.property.property_type import PropertyType


class PropertyCreateSchema(BaseModel):
    name: str = Field(..., description="Nome da propriedade rural")
    size: float = Field(
        ..., gt=0, description="Tamanho em hectares (deve ser maior que zero)"
    )
    property_type: PropertyType = Field(
        ..., description="Tipo da propriedade (DAIRY, BEEF, etc.)"
    )
    owner_id: int = Field(..., description="ID do proprietário (Dono)")
    address_id: int = Field(..., description="ID do endereço da propriedade")


class PropertyUpdateSchema(BaseModel):
    name: Optional[str] = None
    size: Optional[float] = Field(None, gt=0)
    property_type: Optional[PropertyType] = None
    # ADICIONADOS: Agora o Pydantic permite enviar esses IDs no PUT
    owner_id: Optional[int] = None
    address_id: Optional[int] = None


class PropertyResponseSchema(BaseModel):
    id_property: int
    name: str
    area: float  # Sincronizado com o Banco (antigo total_area)
    property_type: str
    owner_id: int  # Sincronizado com o Banco (antigo id_owner)
    address_id: Optional[int] = None

    class Config:
        from_attributes = True  # Permite que o pydantic leia o objeto do SQLAlchemy









































