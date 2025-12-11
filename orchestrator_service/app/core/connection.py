import logging
import os
import psycopg2 as pg
import time

logger = logging.getLogger(__name__)

def pg_connect_with_retry(max_retries=5, delay=5):

    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5434")
    POSTGRES_USER = os.getenv("POSTGRES_USER", "admin")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "1")
    POSTGRES_DB = os.getenv("POSTGRES_DB", "orchestrator-db")

    CREATE_ORCHESTRATOR_TABLE_QUERY = """
    CREATE TABLE IF NOT EXISTS orchestrator (
    id BIGSERIAL PRIMARY KEY,
    tx_id VARCHAR(100) NOT NULL,
    step_name VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    retry_count INT DEFAULT 0,
    request JSONB,
    response JSONB,
    next_retry_at TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW()
);

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
            cursor.execute(CREATE_ORCHESTRATOR_TABLE_QUERY)
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
