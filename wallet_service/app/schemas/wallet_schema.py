from pydantic import BaseModel

class WalletDebitRequest(BaseModel):
    user_id: int
    amount: int

class WalletCreditRequest(BaseModel):
    user_id: int
    amount: int
