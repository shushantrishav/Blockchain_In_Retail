from pydantic import BaseModel
from typing import Optional

class RecordTransactionRequest(BaseModel):
    customer_address: str
    retailer_address: str
    amount_INR: float
    product_id: str
    quantity: int
    description: Optional[str] = ""

class TransactionResponse(BaseModel):
    transaction_id: int
    customer_address: str
    retailer_address: str
    amount_INR: float
    amount_wei: int
    product_id: str
    quantity: int
    timestamp: int
    description: str
    transaction_hash: str
    loyalty_points_awarded: int

class LoyaltyPointsActionRequest(BaseModel):
    customer_address: str
    points_amount: int

class LoyaltyBalanceResponse(BaseModel):
    customer_address: str
    balance: int
