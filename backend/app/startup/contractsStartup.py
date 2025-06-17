from app.services.contractsManager.contract_utils import (
    w3, load_contract, compile_contract, deploy_contract, PRIVATE_KEY
)
from eth_account import Account

# Global contract and deployer variables
retail_transaction_contract = None
loyalty_points_contract = None
deployer_account = None

async def init_contracts():
    """
    Initializes contract instances on app startup.
    Attempts to load deployed contract ABIs and addresses.
    If not found, compiles and deploys the contracts, then loads them.
    """
    global retail_transaction_contract, loyalty_points_contract, deployer_account

    print("🚀 Application starting up...")

    if not w3.is_connected():
        raise Exception("❌ Cannot connect to Ethereum node.")

    deployer_account = Account.from_key(PRIVATE_KEY)
    print(f"🧾 Using deployer account: {deployer_account.address}")

    try:
        # Try loading existing deployed contracts
        retail_transaction_contract = load_contract("RetailTransaction")
        loyalty_points_contract = load_contract("LoyaltyPoints")
        print("✅ Existing contracts loaded successfully.")

    except (FileNotFoundError, ValueError) as e:
        print(f"⚠️  Contracts not found or deployed: {e}\nAttempting to compile and deploy new contracts...")

        try:
            # Compile and deploy RetailTransaction
            retail_abi, retail_bytecode = compile_contract("RetailTransaction", "RetailTransaction.sol")
            deploy_contract(retail_abi, retail_bytecode, deployer_account)
            retail_transaction_contract = load_contract("RetailTransaction")

            # Compile and deploy LoyaltyPoints
            loyalty_abi, loyalty_bytecode = compile_contract("LoyaltyPoints", "LoyaltyPoints.sol")
            deploy_contract(loyalty_abi, loyalty_bytecode, deployer_account)
            loyalty_points_contract = load_contract("LoyaltyPoints")

            print("✅ Contracts compiled, deployed and loaded successfully.")

        except Exception as compile_deploy_error:
            raise Exception(f"❌ Failed to compile and deploy contracts: {compile_deploy_error}")

    if not retail_transaction_contract or not loyalty_points_contract:
        raise Exception("❌ Contracts could not be loaded or deployed during startup.")

    print("✅ Application startup complete. Contracts are ready.")
