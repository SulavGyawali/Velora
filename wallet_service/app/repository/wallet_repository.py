from requests import Session
from app.models.wallet_model import Wallet
import logging
from fastapi import HTTPException

logger = logging.getLogger(__name__)


def check_user_wallet_exists(user_id: int, db: Session) -> bool:
    try:
        wallet = db.query(Wallet).filter(Wallet.user_id == user_id).first()
        logger.info(
            f"Checked wallet existence for user_id {user_id}: {wallet is not None}"
        )
        return wallet is not None
    except Exception as e:
        logger.error(f"Error checking wallet existence for user_id {user_id}: {e}")

        raise HTTPException(status_code=500, detail="Internal server error")


def create_user_wallet(user_id: int, db: Session) -> Wallet:
    try:
        new_wallet = Wallet(user_id=user_id, balance=0)
        db.add(new_wallet)
        db.commit()
        db.refresh(new_wallet)
        logger.info(f"Created wallet for user_id {user_id}")
        return new_wallet
    except Exception as e:
        logger.error(f"Error creating wallet for user_id {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


def get_wallet_by_user_id(user_id: int, db: Session) -> Wallet:
    try:
        wallet = db.query(Wallet).filter(Wallet.user_id == user_id).first()
        logger.info(f"Retrieved wallet for user_id {user_id}")
        return wallet
    except Exception as e:
        logger.error(f"Error retrieving wallet for user_id {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


def debit_wallet(user_id: int, amount: float, db: Session) -> bool:
    try:
        wallet = db.query(Wallet).filter(Wallet.user_id == user_id).first()
        if wallet and wallet.balance >= amount:
            wallet.balance -= amount
            db.commit()
            logger.info(f"Debited {amount} from wallet of user_id {user_id}")
            return True
        else:
            logger.warning(
                f"Insufficient balance for user_id {user_id} or wallet not found"
            )
            raise HTTPException(
                status_code=400, detail="Insufficient balance or wallet not found"
            )
    except Exception as e:
        logger.error(f"Error debiting wallet for user_id {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


def credit_wallet(user_id: int, amount: float, db: Session) -> bool:
    try:
        wallet = db.query(Wallet).filter(Wallet.user_id == user_id).first()
        if wallet:
            wallet.balance += amount
            db.commit()
            logger.info(f"Credited {amount} to wallet of user_id {user_id}")
            return True
        else:
            logger.warning(f"Wallet not found for user_id {user_id}")
            raise HTTPException(status_code=404, detail="Wallet not found")
    except Exception as e:
        logger.error(f"Error crediting wallet for user_id {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
