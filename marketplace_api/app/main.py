from fastapi import FastAPI

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