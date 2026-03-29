from fastapi import FastAPI
from app.database import engine, Base
from app.routes import events, auth

# 1. Logic: This replaces 'db.create_all()' from your Flask code
# It connects to the engine and creates tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Event Ledger API")

# 2. Logic: Register your routes
app.include_router(events.router)
app.include_router(auth.router)
@app.get("/")
async def root():
    return {"message": "FastAPI is running!"}