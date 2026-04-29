from typing import Optional
from pydantic import BaseModel, EmailStr


class UserResponseSchema(BaseModel):
    id_user: int
    name: str
    email: EmailStr
    phone: Optional[str]
    account_status: str
    cpf: str
    address_id: Optional[int]

    class Config:
        from_attributes = True