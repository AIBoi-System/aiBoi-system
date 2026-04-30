from pydantic import BaseModel
from typing import Optional


class AddressBase(BaseModel):
    zip_code: str
    state: str
    neighborhood: str
    street_name: str
    number: str
    complement: Optional[str] = None


class AddressCreate(AddressBase):
    pass


class AddressResponse(AddressBase):
    id_address: int

    class Config:
        from_attributes = True
