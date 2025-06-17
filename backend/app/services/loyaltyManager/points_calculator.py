from app.services.currencyManager.currency_converter import wei_to_INR

POINTS_PER_INR = 1
MIN_INR_FOR_POINTS = 1

def calculate_loyalty_points(amount_in_wei: int) -> int:
    if amount_in_wei < 0:
        raise ValueError("Transaction amount cannot be negative.")

    amount_in_INR = wei_to_INR(amount_in_wei)
    if amount_in_INR < MIN_INR_FOR_POINTS:
        return 0

    points = int(amount_in_INR * POINTS_PER_INR)
    return points
