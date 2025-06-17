from web3 import Web3
from app.services.contractsManager.load_utils import load_contract

async def get_loyalty_balance(customer_address):
    contract = load_contract("LoyaltyPoints")
    balance = contract.functions.getBalance(Web3.to_checksum_address(customer_address)).call()
    return balance
