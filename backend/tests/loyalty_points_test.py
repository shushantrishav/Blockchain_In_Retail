import pytest
import asyncio
from web3 import Web3

from ..contracts.contract_config import w3
from ..loyaltyManager import (
    calculate_loyalty_points,
    award_loyalty_points,
    redeem_loyalty_points,
    get_loyalty_balance
)

@pytest.mark.asyncio
async def test_award_and_redeem_points():
    accounts = w3.eth.accounts
    assert len(accounts) >= 2, "Need at least two Ganache accounts for testing."

    retailer_account = accounts[0]
    customer_account = accounts[1]

    amount_in_wei = Web3.to_wei(0.1, 'ether')  # 0.1 ETH
    points_expected = calculate_loyalty_points(amount_in_wei)

    # Award points
    award_result = await award_loyalty_points(customer_account, amount_in_wei, retailer_account)
    assert award_result["success"], f"Award points transaction failed: {award_result.get('message')}"
    assert award_result["points_awarded"] == points_expected, "Incorrect points awarded"

    # Check balance after awarding
    balance_after_award = await get_loyalty_balance(customer_account)
    assert balance_after_award >= points_expected, "Balance after awarding is incorrect"

    # Redeem points (half of awarded points)
    points_to_redeem = points_expected // 2
    redeem_result = await redeem_loyalty_points(customer_account, points_to_redeem, retailer_account)
    assert redeem_result["success"], f"Redeem points transaction failed: {redeem_result.get('message')}"
    assert redeem_result["points_redeemed"] == points_to_redeem, "Incorrect points redeemed"

    # Check balance after redemption
    balance_after_redeem = await get_loyalty_balance(customer_account)
    assert balance_after_redeem == (balance_after_award - points_to_redeem), "Balance after redemption is incorrect"

@pytest.mark.asyncio
async def test_insufficient_redeem_points():
    accounts = w3.eth.accounts
    retailer_account = accounts[0]
    customer_account = accounts[1]

    # Check initial balance
    balance = await get_loyalty_balance(customer_account)
    # Try to redeem more points than balance
    points_to_redeem = balance + 1000

    redeem_result = await redeem_loyalty_points(customer_account, points_to_redeem, retailer_account)
    assert not redeem_result["success"], "Redemption should have failed for insufficient points"

def test_calculate_points():
    inr_amount = 500.0
    wei_amount = int(inr_amount * 0.0005 * (10**18))  # using your fixed rate logic
    points = calculate_loyalty_points(wei_amount)
    assert points == int(inr_amount), f"Expected {int(inr_amount)} points, got {points}"
