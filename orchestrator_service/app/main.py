from fastapi import FastAPI
from app.core.logging import setup_logging
import logging
from dotenv import load_dotenv
from app.core.connection import pg_connect_with_retry
from app.routes import transaction_route

load_dotenv()

logger = logging.getLogger(__name__)

setup_logging()

app = FastAPI()

try:
    pg_connection = pg_connect_with_retry()
    logger.info("PostgreSQL connection established successfully")
except Exception as e:
    logger.critical(f"Failed to establish PostgreSQL connection: {e}")
    raise e

@app.get("/")
async def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to the Orchestrator Service!"}

app.include_router(transaction_route.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8003)