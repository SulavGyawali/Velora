import redis
from dotenv import load_dotenv
import os
import logging

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

logger = logging.getLogger(__name__)

try:
    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
   
    redis_client.ping()
    logger.info("Connected to Redis successfully")
except redis.RedisError as e:
    logger.error(f"Failed to connect to Redis: {e}")
    redis_client = None