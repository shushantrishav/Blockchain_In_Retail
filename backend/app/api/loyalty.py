from fastapi import APIRouter, HTTPException
from app.startup import contractsStartup as cs
from app.models.schemas import LoyaltyPointsActionRequest, LoyaltyBalanceResponse
from app.services.loyaltyManager.loyalty_util import get_loyalty_balance, redeem_loyalty_points

router = APIRouter(prefix="/loyalty", tags=["Loyalty"])

@router.get("/balance/{customer_address}", response_model=LoyaltyBalanceResponse)
async def get_customer_loyalty_balance(customer_address: str):
    if not cs.loyalty_points_contract:
        raise HTTPException(status_code=500, detail="Loyalty Points contract not initialized.")

    try:
        balance = await get_loyalty_balance(customer_address)
        return LoyaltyBalanceResponse(customer_address=customer_address, balance=balance)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching loyalty balance: {e}")

@router.post("/redeem")
async def redeem_customer_loyalty_points(request: LoyaltyPointsActionRequest):
    if not cs.loyalty_points_contract or not cs.deployer_account:
        raise HTTPException(status_code=500, detail="Loyalty Points contract not initialized or deployer account missing.")

    try:
        result = await redeem_loyalty_points(
            request.customer_address,
            request.points_amount,
            cs.deployer_account
        )
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result.get("message", "Failed to redeem points."))
        return {
            "message": "Loyalty points redeemed successfully",
            "points_redeemed": result["points_redeemed"],
            "transaction_hash": result["transaction_hash"]
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error redeeming loyalty points: {e}")
