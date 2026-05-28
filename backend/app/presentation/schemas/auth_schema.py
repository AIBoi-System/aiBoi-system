from pydantic import BaseModel, EmailStr, Field

from app.presentation.schemas.address_schema import AddressCreate


class LoginRequest(BaseModel):    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str = Field(..., min_length=16)
    new_password: str = Field(..., min_length=8, max_length=128)


class SendVerificationCodeRequest(BaseModel):
    email: EmailStr


class VerifyEmailCodeRequest(BaseModel):
    email: EmailStr
    code: str = Field(..., min_length=5, max_length=5, pattern=r"^\d{5}$")


class RegisterUserRequest(BaseModel):
    name: str = Field(..., min_length=3, max_length=150)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    cpf: str = Field(..., min_length=11, max_length=14)
    phone: str | None = Field(default=None, max_length=20)
    address: AddressCreate