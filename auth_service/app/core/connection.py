import logging
import os
import psycopg2 as pg
import time

logger = logging.getLogger(__name__)


def pg_connect_with_retry(max_retries=5, delay=5):

    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5433")
    POSTGRES_USER = os.getenv("POSTGRES_USER", "admin")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "1")
    POSTGRES_DB = os.getenv("POSTGRES_DB", "wallet-db")

    CREATE_USERS_TABLE_QUERY = """
    CREATE TABLE IF NOT EXISTS users (id serial PRIMARY KEY, username VARCHAR(50), phone VARCHAR(10), password VARCHAR(255), created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, is_verified BOOLEAN DEFAULT FALSE, is_active BOOLEAN DEFAULT TRUE);
    """

    retries = 0
    while retries < max_retries:
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

            return

        except Exception as e:
            logger.error(f"PostgreSQL connection failed: {e}")
            retries += 1
            logger.info(
                f"Retrying in {delay} seconds... (Attempt {retries}/{max_retries})"
            )
            time.sleep(delay)

    raise Exception("Max retries exceeded for PostgreSQL connection")
