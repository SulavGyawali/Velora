from twilio.rest import Client
from dotenv import load_dotenv
import os
import logging

load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

logger = logging.getLogger(__name__)

try:
    if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER]):
        logger.error(
            "Twilio configuration is incomplete. Please set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_PHONE_NUMBER in the environment variables."
        )
        raise EnvironmentError("Twilio configuration is incomplete.")

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    async def send_sms(to_phone_number: str, text: str) -> bool:
        """Send an SMS message using Twilio"""
        try:
            message = client.messages.create(
                body=text, from_=TWILIO_PHONE_NUMBER, to=f"+977{to_phone_number}"
            )
            logger.info(f"SMS sent to +977 {to_phone_number}: SID {message.sid}")
            return True
        except Exception as e:
            logger.error(f"Failed to send SMS to +977 {to_phone_number}: {e}")
            return False

except EnvironmentError as env_err:
    logger.error(f"SMS Service initialization failed: {env_err}")

    def send_sms(to_phone_number: str, message: str) -> bool:
        """Stub function when Twilio is not configured"""
        logger.error("Twilio is not configured. SMS cannot be sent.")
        return False
