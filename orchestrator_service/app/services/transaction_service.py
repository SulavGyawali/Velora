import uuid
import requests
import logging

logger = logging.getLogger(__name__)

wallet_service_url = "http://localhost:8002/wallet"


def generate_transaction_id():
    id = uuid.uuid4()
    tx_id = "tx_" + str(id)
    return tx_id


def credit_user(tx_id: str, user_id: str, amount: float):
    try:
        response = requests.post(
            f"{wallet_service_url}/credit",
            json={
                "tx_id": tx_id,
                "user_id": user_id,
                "amount": amount,
            },
        )
        response.raise_for_status()
        logger.info(f"Credited {amount} to user {user_id} in transaction {tx_id}")

        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error crediting user {user_id}: {e}")
        return {"message": "Failed to credit wallet", "status": "FAILED"}


def debit_user(tx_id: str, user_id: str, amount: float):
    try:
        response = requests.post(
            f"{wallet_service_url}/debit",
            json={
                "tx_id": tx_id,
                "user_id": user_id,
                "amount": amount,
            },
        )
        response.raise_for_status()
        logger.info(f"Debited {amount} from user {user_id} in transaction {tx_id}")

        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error debiting user {user_id}: {e}")
        return {"message": "Failed to debit wallet", "status": "FAILED"}


def transaction(from_user_id: str, to_user_id: str, amount: float):
    tx_id = generate_transaction_id()
    debit_response = debit_user(tx_id, from_user_id, amount)
    if not debit_response or debit_response.get("status") == "FAILED":
        logger.error(
            f"Transaction {tx_id} failed during debit from user {from_user_id}"
        )
        return {"message": "Transaction failed during debit", "status": "FAILED"}

    credit_response = credit_user(tx_id, to_user_id, amount)
    if not credit_response or credit_response.get("status") == "FAILED":
        logger.error(f"Transaction {tx_id} failed during credit to user {to_user_id}")
        refund = credit_user(tx_id, from_user_id, amount)
        if not refund:
            logger.critical(
                f"Failed to refund user {from_user_id} after failed credit to {to_user_id}"
            )
        return {"message": "Transaction failed during credit", "status": "FAILED"}

    return {
        "tx_id": tx_id,
        "from_user_id": from_user_id,
        "to_user_id": to_user_id,
        "amount": amount,
        "status": "SUCCESS",
    }


def get_user_id_by_phone(phone: str):
    try:
        response = requests.get(
            f"http://localhost:8001/auth/users/{phone}",
        )
        response.raise_for_status()
        logger.info(f"Fetched user info for phone {phone}")
        return response.json().get("user_id")
    except requests.RequestException as e:
        logger.error(f"Error fetching user by phone {phone}: {e}")
        return None
    
def log_transaction(
    from_user: str,
    to_user: str,
    amount: float,
    timestamp: str,
    tx_id: str,
):
    try:
        response = requests.post(
            f"{wallet_service_url}/transaction/log",
            json={
                "from_user": from_user,
                "to_user": to_user,
                "amount": amount,
                "timestamp": timestamp,
                "tx_id": tx_id,
            },
        )
        response.raise_for_status()
        logger.info(f"Logged transaction {tx_id} successfully")
        return response.json().get("event_id")
    except requests.RequestException as e:
        logger.error(f"Error logging transaction {tx_id}: {e}")
        return None
