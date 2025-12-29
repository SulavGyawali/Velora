from fastapi import APIRouter, Header
from dotenv import load_dotenv
import os
import logging
import requests

load_dotenv()
logger = logging.getLogger(__name__)

WALLET_URL = os.getenv("WALLET_URL", "http://localhost:8002/wallet")

router = APIRouter(
    prefix="/wallet",
    tags=["wallet"],
)


@router.post("/create")
def create_wallet(Authorization: str = Header(...)):
    if not Authorization:
        logger.error("Authorization token missing")
        return {"error": "Authorization token missing"}

    token = Authorization.split(" ")[1]

    print(token)

    response = requests.post(
        f"{WALLET_URL}/create",
        headers={"Authorization": f"Bearer {token}"},
    )
    if response.status_code == 200:
        logger.info("Wallet created successfully")
        return response.json()
    else:
        logger.error(f"Failed to create wallet: {response.text}")
        return {"error": "Failed to create wallet", "details": response.text}


@router.get("/info")
def get_wallet_info(Authorization: str = Header(...)):
    if not Authorization:
        logger.error("Authorization token missing")
        return {"error": "Authorization token missing"}

    response = requests.get(
        f"{WALLET_URL}/info",
        headers={"Authorization": f"Bearer {Authorization}"},
    )
    if response.status_code == 200:
        logger.info("Fetched wallet info successfully")
        return response.json()
    else:
        logger.error(f"Failed to fetch wallet info: {response.text}")
        return {"error": "Failed to fetch wallet info", "details": response.text}
