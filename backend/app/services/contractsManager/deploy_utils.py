import os
import json
from app.services.contractsManager.contract_config import CONTRACT_BUILD_PATH, w3

def deploy_contract(abi, bytecode, deployer_account, contract_name):
    Contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    nonce = w3.eth.get_transaction_count(deployer_account.address)

    gas_estimate = Contract.constructor().estimate_gas({'from': deployer_account.address})

    tx = Contract.constructor().build_transaction({
        'from': deployer_account.address,
        'nonce': nonce,
        'gas': gas_estimate + 50000,
        'maxFeePerGas': w3.to_wei(20, 'gwei'),
        'maxPriorityFeePerGas': w3.to_wei(2, 'gwei'),
        'chainId': w3.eth.chain_id
    })

    signed_tx = w3.eth.account.sign_transaction(tx, private_key=deployer_account.key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(f"{contract_name} deployment transaction sent: {tx_hash.hex()}")

    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=300)
    print(f"{contract_name} contract deployed at {tx_receipt.contractAddress}")

    abi_path = os.path.join(CONTRACT_BUILD_PATH, f"{contract_name}.abi")
    address_path = os.path.join(CONTRACT_BUILD_PATH, f"{contract_name}.address")

    with open(abi_path, "w") as f:
        json.dump(abi, f)

    with open(address_path, "w") as f:
        f.write(tx_receipt.contractAddress)

    return tx_receipt.contractAddress
