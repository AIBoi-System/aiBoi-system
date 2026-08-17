from typing import Any, List, Optional

from pydantic import BaseModel, EmailStr, field_validator


class OwnerResponseSchema(BaseModel):
    id_user: int
    name: str
    email: EmailStr
    phone: Optional[str] = None
    cpf: str
    subscription_status: str
    properties: List[Any] = []

    @field_validator("cpf")
    @classmethod
    def mask_cpf(cls, v: str) -> str:
        digits = "".join(c for c in v if c.isdigit())
        if len(digits) == 11:
            return f"{digits[:3]}.***.***-{digits[-2:]}"
        return v

    class Config:
        from_attributes = True








































