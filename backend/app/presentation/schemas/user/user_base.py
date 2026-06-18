from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserBaseSchema(BaseModel):
    name: str = Field(..., min_length=3, max_length=150)
    email: EmailStr
    phone: Optional[str] = Field(default=None, max_length=20)
    cpf: str
    address_id: Optional[int] = None








































