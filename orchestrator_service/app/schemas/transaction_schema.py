from pydantic import BaseModel

class TransactionSchema(BaseModel):
    from_user_phone: str
    to_user_phone: str
    amount: float
