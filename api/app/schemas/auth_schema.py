from pydantic import BaseModel

class LoginSchema(BaseModel):
    phone: str
    password: str

    class Config:
        from_attributes = True

class RegisterSchema(LoginSchema):
    username: str

class OTPSchema(BaseModel):
    phone: str

    class Config:
        from_attributes = True

class OTPValidationSchema(OTPSchema):
    otp: str 
