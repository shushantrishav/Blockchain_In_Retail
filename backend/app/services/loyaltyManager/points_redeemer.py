from web3 import Web3
from app.services.contractsManager.load_utils import load_contract
from .balance_checker import get_loyalty_balance
from app.services.contractsManager.contract_config import w3 # Only w3 is needed from config here
from web3 import Account # Needed if you pass an Account object to this function

async def redeem_loyalty_points(customer_address, points, retailer_account_object): # Renamed for clarity
    contract = load_contract("LoyaltyPoints")
    if points <= 0:
        return {"success": False, "message": "Points must be positive."}

    balance = await get_loyalty_balance(customer_address)
    if balance < points:
        return {"success": False, "message": f"Insufficient points. Balance: {balance}, requested: {points}"}

    # --- FIX START ---
    # Use the address attribute for getting nonce
    nonce = w3.eth.get_transaction_count(retailer_account_object.address)
    tx = contract.functions.redeemPoints(
        Web3.to_checksum_address(customer_address),
        points
    ).build_transaction({
        "from": retailer_account_object.address, # Corrected: Use .address
        "gasPrice": w3.eth.gas_price,
        "nonce": nonce,
        "chainId": w3.eth.chain_id,
        "gas": 6000000 # Added a generous gas limit for testing on Ganache
    })

    # Sign the transaction using the private key from the account object
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=retailer_account_object.key)
    
    # Send the raw, signed transaction
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    # --- FIX END ---

    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    return {
        "success": receipt.status == 1,
        "points_redeemed": points,
        "transaction_hash": tx_hash.hex()
    }