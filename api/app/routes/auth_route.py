from fastapi import APIRouter
from dotenv import load_dotenv
import os
from app.schemas.auth_schema import LoginSchema, RegisterSchema, OTPValidationSchema
import requests
import logging

load_dotenv()

logger = logging.getLogger(__name__)

AUTH_URL = os.getenv("AUTH_URL", "http://localhost:8001/auth")
OTP_URL = os.getenv("OTP_SERVICE_URL", "http://localhost:8001/otp")

router = APIRouter()


@router.post("/login")
def login(login_data: LoginSchema):
    print(AUTH_URL)
    response = requests.post(f"{AUTH_URL}/login", json=login_data.dict())
    if response.status_code == 200:
        logger.info("Login successful")
        res = requests.post(
            f"{OTP_URL}/validate", json={"phone": login_data.phone, "otp": ""}
        )
        if res.status_code == 200:
            return res.json()
    else:
        logger.error(f"Login failed: {response.text}")
        return {"error": "Login failed", "details": response.text}


@router.post("/register")
def register(register_data: RegisterSchema):
    response = requests.post(f"{AUTH_URL}/register", json=register_data.dict())
    if response.status_code == 200:
        logger.info("Registration successful")
        return response.json()
    else:
        logger.error(f"Registration failed: {response.text}")
        return {"error": "Registration failed", "details": response.text}


@router.post("/validate-otp")
def validate_otp(otp_data: OTPValidationSchema):
    response = requests.post(f"{OTP_URL}/validate", json=otp_data.dict())
    if response.status_code == 200:
        logger.info("OTP validation successful")
        return response.json()
    else:
        logger.error(f"OTP validation failed: {response.text}")
        return {"error": "OTP validation failed", "details": response.text}
