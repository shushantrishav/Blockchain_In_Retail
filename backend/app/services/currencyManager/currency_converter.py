# backend/app/currency_converter.py
from web3 import Web3

# For demonstration, we'll use a fixed exchange rate.
# In a real-world scenario, you would integrate with a cryptocurrency exchange API
# (e.g., CoinGecko, CoinMarketCap, or a direct exchange API) to get real-time rates.

# Example: 1 ETH = 223044.58 INR (fixed rate for simplicity)
# 1 INR = 0.0000045 ETH
# 1 INR = 0.0005 * 10^18 Wei (since 1 ETH = 10^18 Wei)
FIXED_INR_TO_WEI_RATE = int(0.0000045 * (10**18)) # Wei per INR

def INR_to_wei(INR_amount: float) -> int:
    """
    Converts a INR amount to Wei (the smallest unit of Ether).
    This function uses a fixed conversion rate for demonstration purposes.
    """
    if INR_amount < 0:
        raise ValueError("INR amount cannot be negative.")
    # Calculate Wei amount using the fixed rate
    wei_amount = int(INR_amount * FIXED_INR_TO_WEI_RATE)
    return wei_amount

def wei_to_INR(wei_amount: int) -> float:
    """
    Converts a Wei amount to INR.
    This function uses a fixed conversion rate for demonstration purposes.
    """
    if wei_amount < 0:
        raise ValueError("Wei amount cannot be negative.")
    # Calculate INR amount from Wei
    INR_amount = wei_amount / FIXED_INR_TO_WEI_RATE
    return round(INR_amount, 2) # Round to 2 decimal places for currency

# Example usage (for testing purposes)
if __name__ == "__main__":
    test_INR = 100.0
    wei_val = INR_to_wei(test_INR)
    print(f"{test_INR} INR is {wei_val} Wei")

    test_wei = Web3.to_wei(0.5, 'ether') # Example: 0.5 Ether in Wei
    INR_val = wei_to_INR(test_wei)
    print(f"{test_wei} Wei is {INR_val} INR")

    # Another example using the conversion function itself
    converted_back_INR = wei_to_INR(INR_to_wei(test_INR))
    print(f"Converting {test_INR} INR to Wei and back to INR: {converted_back_INR} INR")
