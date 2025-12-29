from app.core.database import get_mongo_db
import logging
from app.repository.audit_repository import log_audit_event
from fastapi import HTTPException

logger = logging.getLogger(__name__)

mongo_db = get_mongo_db()

def log_wallet_creation(user_id: int, timestamp: str):

    event = {
        "event_type": "wallet_creation",
        "user_id": user_id,
        "timestamp": timestamp,
    }

    try:
        event_id = log_audit_event(event)
        if event_id:
            logger.info(f"Logged wallet creation event: {event}")
            return event_id

        else:
            logger.error("Failed to log wallet creation event")
            raise HTTPException(status_code=500, detail="Internal server error")

    except Exception as e:
        logger.error(f"Error logging wallet creation event: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


def log_wallet_transaction(
    from_user: str,
    to_user: str,
    amount: float,
    timestamp: str,
    tx_id: str,
):

    event = {
        "event_type": "wallet_transaction",
        "transaction_id": tx_id,
        "from_user": from_user,
        "to_user": to_user,
        "amount": amount,
        "timestamp": timestamp,
    }

    try:
        event_id = log_audit_event(event)
        if event_id:
            logger.info(f"Logged wallet transaction event: {event}")
            return event_id

        else:
            logger.error("Failed to log wallet transaction event")
            raise HTTPException(status_code=500, detail="Internal server error")

    except Exception as e:
        logger.error(f"Error logging wallet transaction event: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    

