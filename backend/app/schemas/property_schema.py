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


class PropertyResponseSchema(BaseModel):
    id_property: int
    name: str
    total_area: float  # Como está no banco, talvez revisemos e coloquemos "size"
    property_type: str
    id_owner: int
    id_address: int

    class Config:
        from_attributes = True  # Permite que o pydantic leia o objeto do sqlAlchemy
