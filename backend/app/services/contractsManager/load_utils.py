import os
import json
from web3 import Web3
from app.services.contractsManager.contract_config import w3, CONTRACT_BUILD_PATH

def load_contract(contract_name):
    abi_path = os.path.join(CONTRACT_BUILD_PATH, f"{contract_name}.abi")
    address_path = os.path.join(CONTRACT_BUILD_PATH, f"{contract_name}.address")

    if not os.path.exists(abi_path) or not os.path.exists(address_path):
        raise FileNotFoundError(f"ABI or address file for {contract_name} missing.")

    with open(abi_path, "r") as f:
        abi = json.load(f)

    with open(address_path, "r") as f:
        address = f.read().strip()

    contract = w3.eth.contract(address=Web3.to_checksum_address(address), abi=abi)
    return contract
