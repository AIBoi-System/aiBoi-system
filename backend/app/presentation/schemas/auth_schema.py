from pydantic import BaseModel, EmailStr, Field, field_validator

from app.core.security_validators import (
    normalize_email,
    validate_password_strength,
    validate_safe_text,
)
from app.presentation.schemas.address_schema import AddressCreate


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)

    @field_validator("email")
    @classmethod
    def normalize_login_email(cls, value: str) -> str:
        return normalize_email(str(value))


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    refresh_token: str | None = None
    """Refresh token for obtaining a new access token. Clients should store this
    securely and use /auth/refresh to renew the access token silently."""


class PasswordResetRequest(BaseModel):
    email: EmailStr

    @field_validator("email")
    @classmethod
    def normalize_reset_email(cls, value: str) -> str:
        return normalize_email(str(value))


class PasswordResetConfirm(BaseModel):
    token: str = Field(..., min_length=16, max_length=256)
    new_password: str = Field(..., min_length=8, max_length=128)

    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, value: str) -> str:
        return validate_password_strength(value)


class SendVerificationCodeRequest(BaseModel):
    email: EmailStr

    @field_validator("email")
    @classmethod
    def normalize_signup_email(cls, value: str) -> str:
        return normalize_email(str(value))


class VerifyEmailCodeRequest(BaseModel):
    email: EmailStr
    code: str = Field(..., min_length=5, max_length=5, pattern=r"^\d{5}$")

    @field_validator("email")
    @classmethod
    def normalize_verify_email(cls, value: str) -> str:
        return normalize_email(str(value))


class SendPhoneVerificationCodeRequest(BaseModel):
    phone: str = Field(..., min_length=10, max_length=20)

    @field_validator("phone")
    @classmethod
    def normalize_phone(cls, value: str) -> str:
        digits = "".join(filter(str.isdigit, value))
        if len(digits) not in {10, 11}:
            raise ValueError("Phone must have 10 or 11 digits")
        return digits


class VerifyPhoneCodeRequest(SendPhoneVerificationCodeRequest):
    code: str = Field(..., min_length=5, max_length=5, pattern=r"^\d{5}$")


class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(..., min_length=1, max_length=4096)


class RegisterUserRequest(BaseModel):
    name: str = Field(..., min_length=3, max_length=150)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    cpf: str = Field(..., min_length=11, max_length=14)
    phone: str = Field(..., min_length=10, max_length=20)
    address: AddressCreate

    @field_validator("email")
    @classmethod
    def normalize_register_email(cls, value: str) -> str:
        return normalize_email(str(value))

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        return validate_safe_text(value, "name", max_len=150)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        return validate_password_strength(value)

    @field_validator("cpf")
    @classmethod
    def validate_cpf_digits(cls, value: str) -> str:
        digits = "".join(filter(str.isdigit, value))
        if len(digits) != 11:
            raise ValueError("CPF must contain exactly 11 digits")
        return digits

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str) -> str:
        digits = "".join(filter(str.isdigit, value))
        if len(digits) < 10 or len(digits) > 11:
            raise ValueError("Phone must have 10 or 11 digits")
        return digits


class GoogleLoginRequest(BaseModel):
    id_token: str


class GoogleLoginResponse(BaseModel):
    access_token: str | None = None
    refresh_token: str | None = None
    token_type: str = "bearer"
    role: str | None = None
    email: str | None = None
    name: str | None = None
    needs_registration: bool = False


class GoogleRegisterRequest(BaseModel):
    id_token: str
    cpf: str
    phone: str = Field(..., min_length=10, max_length=20)
    address: AddressCreate

    @field_validator("cpf")
    @classmethod
    def validate_cpf_digits(cls, value: str) -> str:
        digits = "".join(filter(str.isdigit, value))
        if len(digits) != 11:
            raise ValueError("CPF must contain exactly 11 digits")
        return digits

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str) -> str:
        digits = "".join(filter(str.isdigit, value))
        if len(digits) < 10 or len(digits) > 11:
            raise ValueError("Phone must have 10 or 11 digits")
        return digits
