from fastapi import APIRouter
from app.schemas.transaction_schema import TransactionSchema
from app.services.transaction_service import (
    transaction,
    get_user_id_by_phone,
    log_transaction,
)
from datetime import datetime

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
)


@router.get("/")
async def get_transactions():
    return {"message": "List of transactions"}


@router.post("/")
async def create_transaction(tx: TransactionSchema):
    from_user = tx.from_user_phone
    to_user = tx.to_user_phone
    amount = tx.amount

    from_user_id = get_user_id_by_phone(from_user)
    to_user_id = get_user_id_by_phone(to_user)

    result = transaction(from_user_id, to_user_id, amount)

    if not result or result.get("status") == "FAILED":
        return {"message": "Transaction Failed"}

    log_transaction(
        from_user=from_user,
        to_user=to_user,
        amount=amount,
        timestamp=datetime.utcnow().isoformat(),
        tx_id=result.get("tx_id"),
    )

    return {"message": "Transaction Successful", "transaction_id": result.get("tx_id")}
