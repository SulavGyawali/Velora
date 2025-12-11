import psycopg2 as pg
from fastapi import FastAPI
from dotenv import load_dotenv
import os
from app.core.connection import pg_connect_with_retry
from app.core.logging import setup_logging
import time
from app.routes import otp_route, auth_route
import logging

load_dotenv()
setup_logging()

logger = logging.getLogger(__name__)

app = FastAPI()

try:
    pg_connection = pg_connect_with_retry()
    logger.info("PostgreSQL connection established successfully")
except Exception as e:
    logger.critical(f"Failed to establish PostgreSQL connection: {e}")
    raise e


@app.get("/")
async def root():
    return {"message": "Auth Service is running"}


app.include_router(otp_route.router)
app.include_router(auth_route.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8001)
