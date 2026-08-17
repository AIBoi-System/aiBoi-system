import os

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.infrastructure.email.smtp_service import SmtpEmailService
from app.infrastructure.messaging.mailpit_service import (
    MailpitDeliveryService,
    MailpitPhoneSender,
)
from app.shared.application.auth.email_sender import EmailSender
from app.shared.infrastructure.auth.auth import decode_access_token
from app.shared.infrastructure.database.connection import get_db
from app.shared.infrastructure.persistence.user_repository import get_user_by_email
from app.shared.infrastructure.persistence.auth_session import AuthSession
from app.shared.application.auth.phone_sender import LocalPhoneSender, PhoneSender
from app.shared.application.auth.auth_service import AuthService
from app.shared.application.property.property_service import PropertyService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def _delivery_mode() -> str:
    environment = os.getenv("ENV", "development").strip().casefold()
    if environment == "test":
        return "provider"
    configured = os.getenv("AUTH_DELIVERY_MODE", "").strip().casefold()
    if configured:
        if configured not in {"mailpit", "provider"}:
            raise RuntimeError("AUTH_DELIVERY_MODE must be mailpit or provider")
        return configured
    if environment == "development":
        return "mailpit"
    return "provider"


def get_phone_sender() -> PhoneSender:
    if _delivery_mode() == "mailpit":
        return MailpitPhoneSender(MailpitDeliveryService())
    return LocalPhoneSender()


def get_email_sender() -> EmailSender:
    if _delivery_mode() == "mailpit":
        return MailpitDeliveryService()
    return SmtpEmailService()


def get_auth_service(
    db: Session = Depends(get_db),
    phone_sender: PhoneSender = Depends(get_phone_sender),
    email_sender: EmailSender = Depends(get_email_sender),
) -> AuthService:
    return AuthService(db, phone_sender, email_sender)


def _unauthorized() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )


def is_active_user(user) -> bool:
    return str(getattr(user, "account_status", "")).strip().casefold() in {
        "ativo",
        "active",
    }


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    try:
        payload = decode_access_token(token)
    except ValueError as exc:
        raise _unauthorized() from exc

    email = payload.get("sub")
    if not email:
        raise _unauthorized()

    session_id = payload.get("sid")
    auth_session = None
    if session_id:
        auth_session = db.query(AuthSession).filter(AuthSession.id == session_id).first()
        if not auth_session or not auth_session.is_active():
            raise _unauthorized()
    elif os.getenv("ENV", "development").casefold() != "test":
        raise _unauthorized()

    user = get_user_by_email(db, email)
    if not user or not is_active_user(user):
        raise _unauthorized()
    if auth_session and auth_session.user_id != user.id_user:
        raise _unauthorized()
    return user


def get_current_session_id(
    token: str = Depends(oauth2_scheme),
    current_user=Depends(get_current_user),
) -> str:
    del current_user
    try:
        session_id = decode_access_token(token).get("sid")
    except ValueError as exc:
        raise _unauthorized() from exc
    if not session_id:
        raise _unauthorized()
    return str(session_id)


def verify_property_access(db: Session, property_id: int, current_user):
    """Return an accessible property without revealing cross-tenant IDs."""
    if (getattr(current_user, "type", "") or "").casefold() == "admin":
        return PropertyService.get_property_by_id(db, property_id)
    return PropertyService.get_property_by_id(
        db,
        property_id,
        owner_id=current_user.id_user,
    )


def require_roles(*allowed_roles: str):
    def _checker(current_user=Depends(get_current_user)):
        role = (current_user.type or "user").lower()
        if role not in {r.lower() for r in allowed_roles}:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions for this resource.",
            )
        return current_user

    return _checker









































