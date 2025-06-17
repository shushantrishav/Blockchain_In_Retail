from dotenv import load_dotenv
import os
from web3 import Web3

# Load .env file
load_dotenv()

# -------------------------
# Environment & Ethereum Node URL (Ganache)
# -------------------------

# Correctly load the WEB3_PROVIDER from your .env file
# Ensure your .env file has a line like: WEB3_PROVIDER=http://127.0.0.1:7545
WEB3_PROVIDER = os.getenv("WEB3_PROVIDER")

# If you prefer to keep the 'REACT_APP_' prefix in your .env for consistency with a React frontend,
# then you would load it like this instead:
# WEB3_PROVIDER = os.getenv("REACT_APP_WEB3_PROVIDER")

PRIVATE_KEY = os.getenv("PRIVATE_KEY")

if not PRIVATE_KEY:
    raise Exception("Private key not set in environment variables.")

if not WEB3_PROVIDER:
    raise Exception("WEB3_PROVIDER not set in environment variables.")

# -------------------------
# Web3 Provider Setup
# -------------------------
w3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER))

if not w3.is_connected():
    raise Exception(f"Failed to connect to Ethereum node at {WEB3_PROVIDER}. Make sure Server is running.")
else:
    print(f"Connected to Ethereum node at {WEB3_PROVIDER}")

# -------------------------
# Contract Directories
# -------------------------
BASE_CONTRACTS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "contracts"))
CONTRACT_BUILD_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "contract_build")
os.makedirs(CONTRACT_BUILD_PATH, exist_ok=True)