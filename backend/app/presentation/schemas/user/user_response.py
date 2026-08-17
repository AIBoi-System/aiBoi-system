from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator


class UserResponseSchema(BaseModel):
    id_user: int
    name: str
    email: EmailStr
    phone: Optional[str]
    account_status: str
    cpf: str
    address_id: Optional[int]
    type: Optional[str] = "user"

    @field_validator("cpf")
    @classmethod
    def mask_cpf(cls, v: str) -> str:
        digits = "".join(c for c in v if c.isdigit())
        if len(digits) == 11:
            return f"{digits[:3]}.***.***-{digits[-2:]}"
        return v

    class Config:
        from_attributes = True








































