import random
from datetime import timedelta
from app.core.redis import redis_client


class OTPService:
    """Service for generating and validating OTPs."""

    OTP_EXPIRY_DURATION = timedelta(minutes=5)

    @staticmethod
    def generate_otp(phone: str, length: int = 6) -> str:
        """Generate a random OTP of given length."""
        otp = "".join([str(random.randint(0, 9)) for _ in range(length)])
        OTPService.store_otp(phone, otp)
        return otp

    @staticmethod
    def store_otp(phone: str, otp: str):
        """Store the generated OTP in Redis with an expiry."""
        redis_client.setex(
            f"otp:{phone}", int(OTPService.OTP_EXPIRY_DURATION.total_seconds()), otp
        )

    @staticmethod
    def validate_otp(phone: str, otp: str) -> bool:
        """Validate the provided OTP against the stored one."""
        stored_otp = redis_client.get(f"otp:{phone}")
        if stored_otp and stored_otp.decode() == otp:
            redis_client.delete(f"otp:{phone}")
            return True
        return False
