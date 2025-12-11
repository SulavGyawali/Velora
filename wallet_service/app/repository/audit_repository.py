from app.core.database import get_mongo_db
import logging
import uuid

logger = logging.getLogger(__name__)


def log_audit_event(event: dict):
    try:
        mongo_db = get_mongo_db()
        event["event_id"] = str(uuid.uuid4())
        audit_collection = mongo_db.get_collection("audit_logs")
        audit_collection.insert_one(event)
        logger.info(f"Logged audit event: {event}")
        return event["event_id"]
    except Exception as e:
        logger.error(f"Error logging audit event: {e}")
        return None
