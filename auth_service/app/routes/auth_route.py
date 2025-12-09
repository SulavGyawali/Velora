from fastapi import APIRouter, Depends, HTTPException
from requests import Session
from app.services.otp_service import OTPService
from app.services.sms_service import send_sms
from app.schemas.auth_schema import LoginSchema, RegisterSchema
import logging
from app.services.auth_services import verify_password, get_password_hash
from app.repository.user_repository import (
    get_user_by_phone,
    create_user,
    check_user_verification,
)
from app.core.database import get_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login_endpoint(user: LoginSchema, db: Session = Depends(get_db)):
    user = get_user_by_phone(user.phone, db)

    if user is None:
        logger.info(f"User with phone {user.phone} not found")
        raise HTTPException(status_code=403, detail="Invalid credentials")

    if not verify_password(user.password, user.hashed_password):
        logger.info(f"Invalid password for user with phone {user.phone}")
        raise HTTPException(status_code=403, detail="Invalid credentials")

    is_verified = check_user_verification(user.phone, db)

    return {"message": "Login successful", "is_verified": is_verified}


@router.post("/register")
async def register_endpoint(user: RegisterSchema, db: Session = Depends(get_db)):
    try:
        existing_user = get_user_by_phone(user.phone, db)
        if existing_user:
            logger.info(f"User with phone {user.phone} already exists")
            raise HTTPException(status_code=400, detail="User already exists")

        hashed_password = get_password_hash(user.password)

        new_user = create_user(
            username=user.username, phone=user.phone, password=hashed_password, db=db
        )

        otp = OTPService.generate_otp(user.phone)
        otp_message = f"Your OTP code is {otp}"
        success = await send_sms(user.phone, otp_message)
        if success:
            logger.info(f"OTP sent to {user.phone} for registration")
            return {
                "message": f"User registered successfully. OTP sent to {user.phone}"
            }
        else:
            logger.info(f"Failed to send OTP to {user.phone} during registration")
            return {
                "message": f"User registered, but failed to send OTP to {user.phone}"
            }
    except Exception as e:
        logger.error(f"Error during registration for phone {user.phone}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
