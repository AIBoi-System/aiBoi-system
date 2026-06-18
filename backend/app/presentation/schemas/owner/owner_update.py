from typing import Any, List, Optional

from pydantic import BaseModel, EmailStr


class OwnerUpdateSchema(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    cpf: str
    subscription_status: str

class OwnerResponseSchema(BaseModel):
    id_user: int
    name: str
    email: EmailStr
    phone: Optional[str] = None
    cpf: str
    subscription_status: str
    properties: List[Any] = []

    class Config:
        from_attributes = True









































