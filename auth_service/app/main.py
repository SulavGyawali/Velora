import psycopg2 as pg
from fastapi import FastAPI
from dotenv import load_dotenv
import os
import logging
from app.core.logging import setup_logging
import time
from app.routes import otp_route, auth_route

load_dotenv()
setup_logging()

logger = logging.getLogger(__name__)

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_USER = os.getenv("POSTGRES_USER", "admin")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "1")
POSTGRES_DB = os.getenv("POSTGRES_DB", "auth-db")

CREATE_USERS_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS users (id serial PRIMARY KEY, username VARCHAR(50), phone VARCHAR(10), password VARCHAR(255), created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, is_verified BOOLEAN DEFAULT FALSE, is_active BOOLEAN DEFAULT TRUE);
"""

app = FastAPI()

while True:
    try:

        conn = pg.connect(
            host=POSTGRES_HOST,
            port=int(POSTGRES_PORT),
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            database=POSTGRES_DB,
        )

        cursor = conn.cursor()
        cursor.execute(CREATE_USERS_TABLE_QUERY)
        conn.commit()
        cursor.close()

        conn.close()
        logger.info("Database connection successful")

        break
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        logger.info("Retrying in 5 seconds...")

        time.sleep(5)


@app.get("/")
async def root():
    return {"message": "Auth Service is running"}


app.include_router(otp_route.router)
app.include_router(auth_route.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8001)
