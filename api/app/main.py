from fastapi import FastAPI
from app.core.logging import setup_logging
from app.routes.auth_route import router as auth_router
from app.routes.wallet_route import router as wallet_router

setup_logging()

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(auth_router)
app.include_router(wallet_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
