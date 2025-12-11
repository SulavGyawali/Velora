from pydantic import BaseModel

class TransactionSchema(BaseModel):
    from_user_id: str
    to_user_id: str
    amount: float
