from pydantic import BaseModel, EmailStr
from typing import Optional
from app.schemas.address import AddressSchema


class AddressSchema(BaseModel):
    street: str
    number: str
    neighborhood: str
    city: str
    state: str
    zip_code: str

    
class OwnerCreateSchema(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: Optional[str] = None
    cpf: str
    address: Optional[AddressSchema] = None