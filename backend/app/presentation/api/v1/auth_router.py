import logging
import os

from fastapi import APIRouter, Depends, HTTPException, Response, status
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token

from app.presentation.api.auth_dependencies import (
    get_auth_service,
    get_current_session_id,
    get_current_user,
)
from app.presentation.schemas.auth_schema import (
    GoogleLoginRequest,
    GoogleLoginResponse,
    GoogleRegisterRequest,
    LoginRequest,
    PasswordResetConfirm,
    PasswordResetRequest,
    RefreshTokenRequest,
    RegisterUserRequest,
    SendPhoneVerificationCodeRequest,
    SendVerificationCodeRequest,
    TokenResponse,
    VerifyEmailCodeRequest,
    VerifyPhoneCodeRequest,
)
from app.presentation.schemas.user.user_response import UserResponseSchema
from app.shared.application.auth.auth_service import AuthService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["Auth"])


def _tokens(value) -> TokenResponse:
    return TokenResponse(access_token=value.access_token, refresh_token=value.refresh_token, role=value.role)


@router.post("/signup/send-code")
def signup_send_code(payload: SendVerificationCodeRequest, service: AuthService = Depends(get_auth_service)):
    return service.send_email_code(str(payload.email))


@router.post("/signup/verify-code")
def signup_verify_code(payload: VerifyEmailCodeRequest, service: AuthService = Depends(get_auth_service)):
    return service.verify_email_code(str(payload.email), payload.code)


@router.post("/signup/send-phone-code")
def signup_send_phone_code(payload: SendPhoneVerificationCodeRequest, service: AuthService = Depends(get_auth_service)):
    return service.send_phone_code(payload.phone)


@router.post("/signup/verify-phone-code")
def signup_verify_phone_code(payload: VerifyPhoneCodeRequest, service: AuthService = Depends(get_auth_service)):
    return service.verify_phone_code(payload.phone, payload.code)


@router.post("/signup/register", status_code=status.HTTP_201_CREATED)
def signup_register(payload: RegisterUserRequest, service: AuthService = Depends(get_auth_service)):
    user, address_id, tokens = service.register(payload)
    return {"message": "User registered successfully.", "user_id": user.id_user, "address_id": address_id, **_tokens(tokens).model_dump()}


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, service: AuthService = Depends(get_auth_service)):
    return _tokens(service.login(str(payload.email), payload.password))


@router.post("/refresh", response_model=TokenResponse)
def refresh_access_token(payload: RefreshTokenRequest, service: AuthService = Depends(get_auth_service)):
    return _tokens(service.refresh(payload.refresh_token))


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    service: AuthService = Depends(get_auth_service),
    session_id: str = Depends(get_current_session_id),
):
    service.logout(session_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/me", response_model=UserResponseSchema)
def me(current_user=Depends(get_current_user)):
    return current_user


@router.post("/forgot-password")
def forgot_password(payload: PasswordResetRequest, service: AuthService = Depends(get_auth_service)):
    return service.forgot_password(str(payload.email))


@router.post("/reset-password")
def reset_password(payload: PasswordResetConfirm, service: AuthService = Depends(get_auth_service)):
    return service.reset_password(payload.token, payload.new_password)


def _get_google_client_id() -> str:
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    if not client_id:
        raise HTTPException(status_code=500, detail="Google OAuth is not configured on this server.")
    return client_id


def verify_google_token(token: str) -> dict:
    try:
        return id_token.verify_oauth2_token(token, google_requests.Request(), _get_google_client_id())
    except Exception as exc:
        raise HTTPException(status_code=401, detail="Google token verification failed.") from exc


def _verified_google_identity(token: str) -> tuple[str, str]:
    claims = verify_google_token(token)
    email = claims.get("email")
    if not email or claims.get("email_verified") is not True:
        raise HTTPException(status_code=401, detail="Google identity is not verified.")
    return str(email).strip().casefold(), str(claims.get("name") or "Google User")


@router.post("/login/google", response_model=GoogleLoginResponse)
def login_google(payload: GoogleLoginRequest, service: AuthService = Depends(get_auth_service)):
    email, name = _verified_google_identity(payload.id_token)
    tokens = service.google_login(email)
    if not tokens:
        return GoogleLoginResponse(needs_registration=True, email=email, name=name)
    return GoogleLoginResponse(access_token=tokens.access_token, refresh_token=tokens.refresh_token, role=tokens.role, email=email, name=name, needs_registration=False)


@router.post("/register/google", status_code=status.HTTP_201_CREATED)
def register_google(payload: GoogleRegisterRequest, service: AuthService = Depends(get_auth_service)):
    email, name = _verified_google_identity(payload.id_token)
    user, address_id, tokens = service.google_register(name=name, email=email, cpf=payload.cpf, phone=payload.phone, address_payload=payload.address)
    return {"message": "User registered successfully via Google.", "user_id": user.id_user, "address_id": address_id, **_tokens(tokens).model_dump()}
