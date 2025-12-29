from fastapi import Header, HTTPException
import logging
import requests

logger = logging.getLogger(__name__)


def get_current_user_info(token: str) -> dict:
    try:

        if not token:
            logger.warning("Token missing in Authorization header")
            raise HTTPException(
                status_code=401, detail="Token missing in Authorization header"
            )

        response = requests.get(
            f"http://auth-service:8001/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        if response.status_code == 200:
            return response.json()
        else:
            logger.error("Failed to fetch user info from auth service")
            raise HTTPException(status_code=401, detail="Failed to fetch user info")

    except Exception as e:
        logger.error(f"Error fetching user info: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


def get_user_id_from_authorization(Authorization: str = Header(...)) -> int:
    if not Authorization:
        logger.warning("Authorization header missing")
        raise HTTPException(status_code=401, detail="Authorization header missing")

    token = Authorization.split(" ")[1]
    if not token:
        logger.warning("Token missing in Authorization header")
        raise HTTPException(
            status_code=401, detail="Token missing in Authorization header"
        )

    user_info = get_current_user_info(token)
    user_id = user_info.get("user_id")
    if user_id is None:
        logger.warning("Invalid user information extracted from token")
        raise HTTPException(status_code=401, detail="Invalid user information")

    return user_id
