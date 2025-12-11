from pydantic import BaseModel

class UserSchema(BaseModel):
    phone: str

    class Config:
        from_attributes = True

class UserCreateSchema(UserSchema):
    username: str
    password: str

class UserLoginSchema(UserSchema):
    password: str


