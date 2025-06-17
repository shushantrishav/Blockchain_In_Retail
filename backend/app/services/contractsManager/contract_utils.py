from web3 import Account
from .contract_config import w3, PRIVATE_KEY
from .compiler_utils import compile_contract
from .deploy_utils import deploy_contract
from .load_utils import load_contract

def deploy_all():
    # Use the first account from node (Infura testnet doesn’t expose accounts though — note)
    accounts = w3.eth.accounts
    deployer_account = Account.from_key(PRIVATE_KEY)
    print(f"Deployer account: {deployer_account.address}")

    print(f"\nDeployer account: {deployer_account}")

    # Compile and deploy RetailTransaction
    retail_abi, retail_bytecode = compile_contract(
        "RetailTransaction", "RetailTransaction.sol"
    )
    retail_contract_address = deploy_contract(
        retail_abi, retail_bytecode, deployer_account, "RetailTransaction"
    )
    print(f"RetailTransaction contract deployed at {retail_contract_address}")

    # Compile and deploy LoyaltyPoints
    loyalty_abi, loyalty_bytecode = compile_contract(
        "LoyaltyPoints", "LoyaltyPoints.sol"
    )
    loyalty_contract_address = deploy_contract(
        loyalty_abi, loyalty_bytecode, deployer_account, "LoyaltyPoints"
    )
    print(f"LoyaltyPoints contract deployed at {loyalty_contract_address}")

    # Load contracts to verify
    retail_contract = load_contract("RetailTransaction")
    loyalty_contract = load_contract("LoyaltyPoints")

    print(f"\nContracts loaded successfully:\n- RetailTransaction: {retail_contract.address}\n- LoyaltyPoints: {loyalty_contract.address}")

if __name__ == "__main__":
    deploy_all()
