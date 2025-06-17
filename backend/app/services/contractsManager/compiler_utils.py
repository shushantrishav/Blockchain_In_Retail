import os
import json
from solcx import compile_standard, install_solc, get_installed_solc_versions
from .contract_config import BASE_CONTRACTS_PATH, CONTRACT_BUILD_PATH

# Solidity version to use
SOLC_VERSION = "0.8.0"

# Install solc compiler if not already installed
if SOLC_VERSION not in get_installed_solc_versions():
    print(f"📦 Installing Solidity compiler {SOLC_VERSION}...")
    install_solc(SOLC_VERSION)

def compile_contract(contract_name: str, relative_contract_path: str):
    contract_full_path = os.path.join(BASE_CONTRACTS_PATH, relative_contract_path)
    if not os.path.exists(contract_full_path):
        raise FileNotFoundError(f"❌ Contract not found: {contract_full_path}")

    # Read contract source code
    with open(contract_full_path, "r") as f:
        source_code = f.read()

    # Compile the contract
    compiled = compile_standard(
        {
            "language": "Solidity",
            "sources": {relative_contract_path: {"content": source_code}},
            "settings": {
                "outputSelection": {
                    "*": {
                        "*": ["abi", "evm.bytecode.object"]
                    }
                }
            },
        },
        solc_version=SOLC_VERSION
    )

    # Extract ABI and Bytecode
    abi = compiled["contracts"][relative_contract_path][contract_name]["abi"]
    bytecode = compiled["contracts"][relative_contract_path][contract_name]["evm"]["bytecode"]["object"]

    # Save ABI
    abi_path = os.path.join(CONTRACT_BUILD_PATH, f"{contract_name}.abi")
    with open(abi_path, "w") as f:
        json.dump(abi, f)

    # Save Bytecode
    bin_path = os.path.join(CONTRACT_BUILD_PATH, f"{contract_name}.bin")
    with open(bin_path, "w") as f:
        f.write(bytecode)

    print(f"✅ Compiled {contract_name}. ABI saved to {abi_path}, Bytecode saved to {bin_path}")

    return abi, bytecode
