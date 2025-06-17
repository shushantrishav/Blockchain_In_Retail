from fastapi import FastAPI
from app.api import transactions, loyalty,status
from app.startup import contractsStartup
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Retail Blockchain System API",
    description="API for managing retail transactions and loyalty points on the blockchain.",
    version="1.0.0",
)

# CORS configuration
origins = [
    "http://localhost:3000",        # for local React/Vue/Next frontend
    # "https://your-frontend-url.com" # your Render frontend URL (if deploying)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,             # or ["*"] for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
