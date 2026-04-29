from typing import Optional
from pydantic import BaseModel, Field


class UserUpdateSchema(BaseModel):
    name: Optional[str] = Field(default=None, min_length=3, max_length=150)
    phone: Optional[str] = Field(default=None, max_length=20)
    account_status: Optional[str] = None
    address_id: Optional[int] = None