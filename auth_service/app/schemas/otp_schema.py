from pydantic import BaseModel

class OTPSchema(BaseModel):
    phone: str

    class Config:
        from_attributes = True

class OTPValidationSchema(OTPSchema):
    otp: str 