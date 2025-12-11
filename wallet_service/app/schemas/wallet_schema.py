from pydantic import BaseModel

class WalletDebitSchema(BaseModel):
    tx_id: str
    user_id: int
    amount: int

class WalletCreditSchema(BaseModel):
    tx_id: str
    user_id: int
    amount: int

class WalletTransactionLogSchema(BaseModel):
    from_user: str
    to_user: str
    amount: float
    timestamp: str
    tx_id: str