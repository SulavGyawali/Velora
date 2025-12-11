import logging
import psycopg2 as pg
import os
import time
from dotenv import load_dotenv
from pymongo import MongoClient
from fastapi import HTTPException

load_dotenv()

logger = logging.getLogger(__name__)


def pg_connect_with_retry(max_retries=5, delay=5):

    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5433")
    POSTGRES_USER = os.getenv("POSTGRES_USER", "admin")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "1")
    POSTGRES_DB = os.getenv("POSTGRES_DB", "wallet-db")

    CREATE_WALLETS_TABLE_QUERY = """
    CREATE TABLE IF NOT EXISTS wallets (id serial PRIMARY KEY, user_id INT, balance DECIMAL DEFAULT 0, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
        """

    CREATE_TRANSACTIONS_TABLE_QUERY = """
    CREATE TABLE IF NOT EXISTS transactions (id serial PRIMARY KEY, tx_id VARCHAR(50), user_id INT, amount DECIMAL, transaction_type VARCHAR(10), status VARCHAR(20), created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
        """

    retries = 0
    while retries < max_retries:
        try:
            connection = pg.connect(
                host=POSTGRES_HOST,
                port=POSTGRES_PORT,
                user=POSTGRES_USER,
                password=POSTGRES_PASSWORD,
                database=POSTGRES_DB,
            )
            logger.info("PostgreSQL connection successful")

            cur = connection.cursor()
            cur.execute(CREATE_WALLETS_TABLE_QUERY)
            cur.execute(CREATE_TRANSACTIONS_TABLE_QUERY)
            connection.commit()
            cur.close()

            return connection

        except Exception as e:
            logger.error(f"PostgreSQL connection failed: {e}")
            retries += 1
            logger.info(
                f"Retrying in {delay} seconds... (Attempt {retries}/{max_retries})"
            )
            time.sleep(delay)

    raise HTTPException(status_code=500, detail="Max retries exceeded for PostgreSQL connection")


def mongo_connect_with_retry(max_retries=5, delay=5):

    MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
    MONGO_PORT = int(os.getenv("MONGO_PORT", "27017"))
    MONGO_USER = os.getenv("MONGO_USER", "admin")
    MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "1")
    MONGO_DB = os.getenv("MONGO_DB", "wallet-db")

    retries = 0
    while retries < max_retries:
        try:
            mongo_client = MongoClient(
                host=MONGO_HOST,
                port=MONGO_PORT,
                username=MONGO_USER,
                password=MONGO_PASSWORD,
            )
            mongo_db = mongo_client[MONGO_DB]
            mongo_client.admin.command("ping")
            logger.info("MongoDB connection successful")
            return mongo_db
        except Exception as e:
            logger.error(f"MongoDB connection failed: {e}")
            retries += 1
            logger.info(
                f"Retrying in {delay} seconds... (Attempt {retries}/{max_retries})"
            )
            time.sleep(delay)

    raise HTTPException(status_code=500, detail="Max retries exceeded for MongoDB connection")
