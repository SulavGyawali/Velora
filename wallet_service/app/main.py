from fastapi import FastAPI
from app.core.logging import setup_logging
import logging
from app.core.database import init_db_connections
from app.routes import wallet_route

setup_logging()

logger = logging.getLogger(__name__)

app = FastAPI()
app.add_event_handler("startup", init_db_connections)

@app.get("/")
async def root():
    return {"message": "Wallet Service is running"}

app.include_router(wallet_route.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8002)
