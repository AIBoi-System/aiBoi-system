from pydantic import BaseModel, EmailStr
from typing import Optional


from app.presentation.schemas.address_schema import AddressCreate


class OwnerCreateSchema(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: Optional[str] = None
    cpf: str
    # E usamos o nome exato aqui também!
    address: Optional[AddressCreate] = None
    subscription_status: str


class OwnerResponseSchema(BaseModel):
    id_owner: int
    id_user: int
    subscription_status: str

    class Config:
        from_attributes = True









































