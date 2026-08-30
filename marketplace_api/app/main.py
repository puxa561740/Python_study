from fastapi import FastAPI
from sqlalchemy import text

from app.api.v1.auth import router as auth_router
from app.core.database import engine

app = FastAPI(
    title="Marketplace API",
    description="Backend API интернет-магазина",
    version="1.0.0",
)

@app.get("/")
def read_root():
    return {
        "message": "Marketplace API is running"
    }

@app.get("/health/database")
def database_health():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))

    return {
        "database": result.scalar()
    }

app.include_router(
    auth_router,
    prefix="/api/v1",
)