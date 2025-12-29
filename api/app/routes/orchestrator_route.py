from fastapi import APIRouter
from dotenv import load_dotenv
import os
import logging 

load_dotenv()
logger = logging.getLogger(__name__)

ORCHESTRATOR_URL = os.getenv("ORCHESTRATOR_URL", "http://localhost:8002/orchestrator")