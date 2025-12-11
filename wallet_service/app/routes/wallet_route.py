from fastapi import APIRouter, Depends, HTTPException
from app.core.database import postgres_db
from requests import Session
from app.repository.wallet_repository import (
    check_user_wallet_exists,
    create_user_wallet,
    get_wallet_by_user_id,
    debit_wallet,
    credit_wallet,
)
from app.repository.transaction_repository import log_transaction, get_transaction
import logging
from app.schemas.wallet_schema import (
    WalletDebitSchema,
    WalletCreditSchema,
    WalletTransactionLogSchema,
)
from app.core.dependencies import get_user_id_from_authorization, get_current_user_info
from app.services.audit_service import log_wallet_creation, log_wallet_transaction

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/wallet",
    tags=["wallet"],
)


@router.post("/create")
async def create_wallet_route(
    user_id: int = Depends(get_user_id_from_authorization),
    db: Session = Depends(postgres_db),
):
    try:
        wallet_exists = check_user_wallet_exists(user_id, db)
        if wallet_exists:
            logger.info(f"Wallet already exists for user_id {user_id}")
            return {"message": "Wallet already exists"}

        wallet = create_user_wallet(user_id, db)
        if wallet is None:
            logger.error(f"Failed to create wallet for user_id {user_id}")
            return {"message": "Failed to create wallet"}
        logger.info(f"Creating wallet for user_id {user_id}")
        log_wallet_creation(
            user_id=user_id,
            wallet_id=wallet["wallet_id"],
            timestamp=wallet["created_at"].isoformat(),
        )
        return {"message": "Wallet created", "user_id": user_id}
    except HTTPException as e:
        logger.error(
            f"HTTP error while creating wallet for user_id {user_id}: {e.detail}"
        )
        raise e
    except Exception as e:
        logger.error(f"Error creating wallet for user_id {user_id}: {e}")
        return {"message": "Failed to create wallet"}


@router.get("/info")
async def get_wallet_route(
    user_info: dict = Depends(get_current_user_info), db: Session = Depends(postgres_db)
):
    try:
        user_id = user_info["user_id"]
        wallet_exists = check_user_wallet_exists(user_id, db)

        if not wallet_exists:
            logger.info(f"No wallet found for user_id {user_id}")
            return {"message": "No wallet found"}

        wallet = get_wallet_by_user_id(user_id, db)
        if wallet is None:
            logger.error(f"Failed to retrieve wallet for user_id {user_id}")
            return {"message": "Failed to retrieve wallet"}

        return {"wallet": wallet}
    except HTTPException as e:
        logger.error(
            f"HTTP error while retrieving wallet for user_id {user_id}: {e.detail}"
        )
        raise e
    except Exception as e:
        logger.error(f"Error retrieving wallet for user_id {user_id}: {e}")
        return {"message": "Failed to retrieve wallet"}


@router.post("/debit")
async def debit_wallet_route(
    debit_request: WalletDebitSchema,
    db: Session = Depends(postgres_db),
):
    try:
        existing_tx = get_transaction(
            tx_id=debit_request.tx_id,
            tx_type="debit",
            db=db,
            user_id=debit_request.user_id,
        )

        if existing_tx:
            logger.info(
                f"Duplicate debit transaction detected for tx_id {debit_request.tx_id}"
            )
            return {"message": "Duplicate transaction"}

        debit = debit_wallet(debit_request.user_id, debit_request.amount, db)
        if debit:
            logger.info(
                f"Debited {debit_request.amount} from wallet of user_id {debit_request.user_id}"
            )
            log_transaction(
                user_id=debit_request.user_id,
                tx_id=debit_request.tx_id,
                amount=debit_request.amount,
                tx_type="debit",
                db=db,
                status="completed",
            )
            return {
                "message": "Wallet debited successfully",
                "amount": debit_request.amount,
                "status": "COMPLETED",
            }
        else:
            logger.warning(f"Failed to debit wallet of user_id {debit_request.user_id}")
            return {"message": "Failed to debit wallet", "status": "FAILED"}
    except HTTPException as e:
        logger.error(
            f"HTTP error while debiting wallet for user_id {debit_request.user_id}: {e.detail}"
        )
        raise e
    except Exception as e:
        logger.error(f"Error debiting wallet for user_id {debit_request.user_id}: {e}")
        return {"message": "Failed to debit wallet", "status": "FAILED"}


@router.post("/credit")
async def credit_wallet_route(
    credit_request: WalletCreditSchema,
    db: Session = Depends(postgres_db),
):
    try:
        existing_tx = get_transaction(
            tx_id=credit_request.tx_id,
            tx_type="credit",
            db=db,
            user_id=credit_request.user_id,
        )

        if existing_tx:
            logger.info(
                f"Duplicate credit transaction detected for tx_id {credit_request.tx_id}"
            )
            return {"message": "Duplicate transaction"}

        credit = credit_wallet(credit_request.user_id, credit_request.amount, db)
        if credit:
            logger.info(
                f"Credited {credit_request.amount} to wallet of user_id {credit_request.user_id}"
            )
            log_transaction(
                user_id=credit_request.user_id,
                tx_id=credit_request.tx_id,
                amount=credit_request.amount,
                tx_type="credit",
                db=db,
                status="completed",
            )
            return {
                "message": "Wallet credited successfully",
                "amount": credit_request.amount,
                "status": "COMPLETED",
            }
        else:
            logger.warning(
                f"Failed to credit wallet of user_id {credit_request.user_id}"
            )
            return {"message": "Failed to credit wallet", "status": "FAILED"}
    except HTTPException as e:
        logger.error(
            f"HTTP error while crediting wallet for user_id {credit_request.user_id}: {e.detail}"
        )
        raise e
    except Exception as e:
        logger.error(
            f"Error crediting wallet for user_id {credit_request.user_id}: {e}"
        )
        return {"message": "Failed to credit wallet", "status": "FAILED"}


@router.post("/transaction/log")
async def log_wallet_transaction_route(
    transaction_log: WalletTransactionLogSchema,
):
    try:
        event_id = log_wallet_transaction(
            from_user=transaction_log.from_user,
            to_user=transaction_log.to_user,
            amount=transaction_log.amount,
            timestamp=transaction_log.timestamp,
            tx_id=transaction_log.tx_id,
        )
        if event_id is None:
            logger.error(f"Failed to log transaction for tx_id {transaction_log.tx_id}")
            return {"message": "Failed to log transaction"}
        return {"message": "Transaction logged", "event_id": event_id}
    except HTTPException as e:
        logger.error(
            f"HTTP error while logging transaction for tx_id {transaction_log.tx_id}: {e.detail}"
        )
        raise e
    except Exception as e:
        logger.error(
            f"Error logging transaction for tx_id {transaction_log.tx_id}: {e}"
        )
        return {"message": "Failed to log transaction"}
