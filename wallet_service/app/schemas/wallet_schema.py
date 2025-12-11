from pydantic import BaseModel

class WalletDebitRequest(BaseModel):
    tx_id: str
    user_id: int
    amount: int

class WalletCreditRequest(BaseModel):
    tx_id: str
    user_id: int
    amount: int
