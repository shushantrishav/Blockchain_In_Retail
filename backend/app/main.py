from fastapi import FastAPI
from app.api import transactions, loyalty, status
from app.startup import contractsStartup
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Allowed frontend origins from .env
origins = os.getenv("ALLOWED_ORIGINS", "").split(",")

app = FastAPI(
    title="Retail Blockchain System API",
    description="API for managing retail transactions and loyalty points on the blockchain.",
    version="1.0.0",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,        
    allow_methods=["GET", "POST"],     
    allow_headers=["Authorization", "Content-Type"],
)

@app.on_event("startup")
async def startup_event():
    await contractsStartup.init_contracts()

app.include_router(status.router)
app.include_router(transactions.router)
app.include_router(loyalty.router)

@app.get("/")
def read_root():
    return {"message": "Retail Blockchain System API is running!"}
