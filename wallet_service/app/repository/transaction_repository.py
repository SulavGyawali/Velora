from app.models.transaction_model import Transaction
from requests import Session
import logging
from fastapi import HTTPException

logger = logging.getLogger(__name__)


def log_transaction(
    user_id: int, tx_id: str, amount: float, tx_type: str, status: str, db: Session
) -> Transaction:
    try:
        new_transaction = Transaction(
            user_id=user_id,
            tx_id=tx_id,
            amount=amount,
            transaction_type=tx_type,
            status=status,
        )
        db.add(new_transaction)
        db.commit()
        db.refresh(new_transaction)
        logger.info(
            f"Logged {tx_type} transaction for user_id {user_id} with tx_id {tx_id} and amount {amount}"
        )
        return new_transaction
    except Exception as e:
        logger.error(
            f"Error logging transaction for user_id {user_id} with tx_id {tx_id}: {e}"
        )
        raise HTTPException(status_code=500, detail="Internal server error")


def get_transaction(
    tx_id: str, tx_type: str, db: Session, user_id: int = None
) -> Transaction:
    try:
        transaction_query = (
            db.query(Transaction)
            .filter(Transaction.tx_id == tx_id, Transaction.transaction_type == tx_type)
            .first()
        )

        if user_id is not None and transaction_query:
            transaction = transaction_query.filter(
                Transaction.user_id == user_id
            ).first()
        else:
            transaction = transaction_query

        if transaction:
            logger.info(f"Retrieved transaction with tx_id {tx_id}")
        else:
            logger.warning(f"No transaction found with tx_id {tx_id}")
        return transaction
    except Exception as e:
        logger.error(f"Error retrieving transaction with tx_id {tx_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
