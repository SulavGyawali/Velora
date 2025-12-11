from fastapi import APIRouter
from app.schemas.transaction_schema import TransactionSchema
from app.services.transaction_service import transaction

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
)


@router.get("/")
async def get_transactions():
    return {"message": "List of transactions"}


@router.post("/")
async def create_transaction(tx: TransactionSchema):
    from_user = tx.from_user_id
    to_user = tx.to_user_id
    amount = tx.amount
    result = transaction(from_user, to_user, amount)

    if not result or result.get("status") == "FAILED":
        return {"message": "Transaction failed"}

    return {"message": "Transaction created"}
