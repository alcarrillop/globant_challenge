from fastapi import FastAPI
from .routes import router
from .database import create_tables

app = FastAPI(
    title="DB Migration API",
    description="API for migrating CSV data to PostgreSQL database",
    version="1.0.0"
)

# Include routes
app.include_router(router)

# Create tables on startup
@app.on_event("startup")
async def startup_event():
    create_tables()
