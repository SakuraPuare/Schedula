from app.api.dependencies import token_service
from app.core.settings import get_settings
from app.services.mail_service import EmailVerificationService


async def send_verify_email(receiver_email: str, receiver_type: str):
    EmailVerificationService(get_settings(), token_service).send_verification_email(
        receiver_email,
        receiver_type,
    )
