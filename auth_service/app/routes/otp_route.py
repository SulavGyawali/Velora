from fastapi import APIRouter, Depends
from app.services.otp_service import OTPService
from app.services.sms_service import send_sms
from app.schemas.otp_schema import OTPSchema, OTPValidationSchema
from app.services.oauth_service import create_access_token
import logging
from app.repository.user_repository import (
    get_user_by_phone,
    update_user_verification,
)
from app.core.database import get_db

router = APIRouter(prefix="/otp", tags=["otp"])

logger = logging.getLogger(__name__)


@router.post("/send")
async def send_otp_endpoint(otp_data: OTPSchema):
    otp = OTPService.generate_otp(otp_data.phone)
    otp_message = f"Your OTP code is {otp}"
    success = await send_sms(otp_data.phone, otp_message)
    if success:
        logger.info(f"OTP sent to {otp_data.phone}")
        return {"message": f"OTP sent to {otp_data.phone}"}
    else:
        logger.info(f"Failed to send OTP to {otp_data.phone}")
        return {"message": f"Failed to send OTP to {otp_data.phone}"}


@router.post("/validate")
def validate_otp_endpoint(otp_data: OTPValidationSchema, db=Depends(get_db)):
    try:
        if OTPService.validate_otp(otp_data.phone, otp_data.otp):
            user = get_user_by_phone(otp_data.phone, db)
            update_user_verification(otp_data.phone, True, db)
            sub = {
                "user_id": user.id,
                "phone": user.phone,
                "is_verified": user.is_verified,
            }
            access_token = create_access_token(data={"sub": sub})
            logger.info(f"OTP validated for phone number {otp_data.phone}")
            return {"message": "OTP is valid", "access_token": access_token}
        else:
            logger.info(f"Invalid OTP attempt for phone number {otp_data.phone}")
            return {"message": "OTP is invalid"}
    except Exception as e:
        logger.error(f"Error validating OTP for phone number {otp_data.phone}: {e}")
        return {"message": "Error validating OTP"}
