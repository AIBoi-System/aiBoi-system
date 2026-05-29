from typing import Optional

from pydantic import BaseModel, Field, field_validator

from app.core.security_validators import (
    validate_safe_text,
    validate_state_uf,
    validate_zip_code,
)


class AddressBase(BaseModel):
    zip_code: str = Field(..., max_length=20)
    state: str = Field(..., max_length=2)
    neighborhood: str = Field(..., max_length=100)
    street_name: str = Field(..., max_length=150)
    number: str = Field(..., max_length=20)
    complement: Optional[str] = Field(default=None, max_length=255)

    @field_validator("zip_code")
    @classmethod
    def validate_zip(cls, value: str) -> str:
        return validate_zip_code(value)

    @field_validator("state")
    @classmethod
    def validate_state(cls, value: str) -> str:
        return validate_state_uf(value)

    @field_validator("neighborhood", "street_name")
    @classmethod
    def validate_address_text(cls, value: str) -> str:
        return validate_safe_text(value, "address field", max_len=150)

    @field_validator("number")
    @classmethod
    def validate_number(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned or len(cleaned) > 20:
            raise ValueError("Number is invalid")
        return cleaned

    @field_validator("complement")
    @classmethod
    def validate_complement(cls, value: Optional[str]) -> Optional[str]:
        if value is None or value.strip() == "":
            return None
        return validate_safe_text(value, "complement", max_len=255)


class AddressCreate(AddressBase):
    pass


class AddressUpdate(BaseModel):
    zip_code: Optional[str] = None
    state: Optional[str] = None
    neighborhood: Optional[str] = None
    street_name: Optional[str] = None
    number: Optional[str] = None
    complement: Optional[str] = None


class AddressResponse(AddressBase):
    id_address: int

    class Config:
        from_attributes = True
