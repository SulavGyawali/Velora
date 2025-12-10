from pydantic import BaseModel

class LoginSchema(BaseModel):
    phone: str
    password: str

    class Config:
        from_attributes = True

class RegisterSchema(LoginSchema):
    username: str

