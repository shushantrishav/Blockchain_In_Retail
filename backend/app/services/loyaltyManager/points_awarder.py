from web3 import Web3
from app.services.contractsManager.load_utils import load_contract
from .balance_checker import get_loyalty_balance
from .points_calculator import calculate_loyalty_points
from app.services.contractsManager.contract_config import w3

async def award_loyalty_points(customer_address, amount_in_wei, retailer_account):
    contract = load_contract("LoyaltyPoints")
    points = calculate_loyalty_points(amount_in_wei)

    if points <= 0:
        return {"success": True, "points_awarded": 0, "message": "No points awarded"}

    nonce = w3.eth.get_transaction_count(retailer_account)
    tx = contract.functions.awardPoints(
        Web3.to_checksum_address(customer_address),
        points
    ).build_transaction({
        "from": retailer_account,
        "gasPrice": w3.eth.gas_price,
        "nonce": nonce,
        "chainId": w3.eth.chain_id
    })

    tx_hash = w3.eth.send_transaction(tx)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    return {
        "success": receipt.status == 1,
        "points_awarded": points,
        "transaction_hash": tx_hash.hex()
    }
