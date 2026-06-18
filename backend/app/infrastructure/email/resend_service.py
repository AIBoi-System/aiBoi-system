import logging
import os
import resend

logger = logging.getLogger(__name__)

class ResendEmailService:
    """Sends transactional email via Resend API."""
    
    def __init__(self) -> None:
        resend.api_key = os.getenv("RESEND_API_KEY", "")
        self._from_email = os.getenv("RESEND_FROM_EMAIL", "onboarding@resend.dev")

    @property
    def is_configured(self) -> bool:
        return bool(resend.api_key and self._from_email)

    def send_verification_code(self, to_email: str, code: str) -> None:
        subject = "AiBoi - Código de Verificação"
        
        # O Resend permite enviar HTML puro muito facilmente
        html_body = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2>Bem-vindo ao AiBoi! 🐂</h2>
            <p>Seu código de verificação para concluir o cadastro é:</p>
            <h1 style="background: #f4f4f4; padding: 10px; text-align: center; letter-spacing: 5px;">{code}</h1>
            <p style="color: #666; font-size: 12px;">Este código expira em 15 minutos.</p>
        </div>
        """
        self._send(to_email, subject, html_body)

    def _send(self, to_email: str, subject: str, html_body: str) -> None:
        env = os.getenv("ENV", "development")
        
        if not self.is_configured:
            if env == "production":
                raise RuntimeError("Resend API is not configured for production")
            logger.warning("Resend not configured; email to %s was not sent", to_email)
            return

        params = {
            "from": self._from_email,
            "to": [to_email],
            "subject": subject,
            "html": html_body,
        }

        try:
            resend.Emails.send(params)
        except Exception as exc:
            logger.exception("Failed to send email to %s via Resend", to_email)
            raise RuntimeError("Unable to send verification email") from exc








































