
# 🚀 Retail Blockchain System

A decentralized, transparent, and secure platform for managing retail transactions and loyalty points using blockchain technology.

---

## 📌 1️⃣ Problem Statement

Traditional retail systems often suffer from:

- **Lack of Transparency:** Unclear data usage and loyalty point management.
- **Centralized Control:** Vulnerable to breaches and arbitrary rule changes.
- **Interoperability Issues:** Loyalty points locked within single brands.
- **Fraud and Disputes:** No immutable transaction records.
- **Inefficient Record Keeping:** Expensive, slow databases for large transaction volumes.

**✅ Solution:** Leverage blockchain to provide decentralized, transparent, and tamper-proof retail transaction management.

---

## 📌 2️⃣ Technology Stack & Rationale

| Technology         | Purpose                                                         | Why?                                                                                   |
|:------------------|:---------------------------------------------------------------|:----------------------------------------------------------------------------------------|
| **Solidity**       | Smart contract programming language.                            | Standard for EVM-based blockchains.                                                     |
| **Ethereum/Ganache** | Blockchain platform for transaction and loyalty records.        | Decentralized ledger with local dev support via Ganache.                                |
| **FastAPI**        | Web API framework (Python 3.7+).                                | High-performance, async support, automatic interactive docs.                           |
| **Web3.py**        | Ethereum blockchain interaction library.                        | Connects to Ethereum nodes, manages smart contracts and transactions.                  |
| **Pydantic**       | Data validation and management.                                 | Robust validation for API requests and responses.                                       |
| **python-dotenv**  | Environment variable management.                                | Safely handles sensitive config like private keys.                                      |
| **solcx**          | Solidity compiler wrapper for Python.                          | Compiles smart contracts programmatically.                                              |
| **Docker**         | Containerization platform.                                      | Consistent, portable deployment environment.                                            |

---

## 📌 3️⃣ High-Level Design (HLD)

```
+--------------------+         +----------------------------+         +-----------------------+
| Frontend (Optional)|         |   FastAPI Backend (Python) |         | Ethereum Blockchain   |
| (e.g., React/Vue)  |         |                            |         | (Ganache for Dev)     |
+--------+-----------+         +------------+---------------+         +-----------+-----------+
         |                                  |                                      |
         |  HTTP Requests (API Calls)       | REST Endpoints                       | Smart Contract Calls
         |--------------------------------->+--(/transactions, /loyalty, /status)--|--------------------------->
         |                                  |                                      |  - RetailTransaction.sol
         |                                  |                                      |  - LoyaltyPoints.sol
         |                                  |                                      |
         |<---------------------------------| API Responses                        |<---------------------------
         |  Data / Status                   |                                      |  Transaction Receipts
         |                                  |                                      |  Loyalty Balances
         |                                  |                                      |
+--------+---------+           +------------+---------------+         +-----------+-----------+
                                            |
                                            | Services:
                                            | - Contracts Manager (compile, deploy, load)
                                            | - Currency Converter (INR <-> Wei)
                                            | - Loyalty Manager (calculate, award, redeem, check)
                                            | - Transaction Manager (match off-chain IDs)
                                            |
                                            | Startup:
                                            | - Initializes/Deploys Contracts
                                            |
                                            | Models:
                                            | - Pydantic Schemas
```

**Services:**

- Contract Manager  
- Currency Converter (INR ↔ Wei)  
- Loyalty Manager (award/redeem/check points)  
- Transaction Manager (map off-chain IDs)  

**Workflow:**

1. **Startup:** Compile & deploy smart contracts or load existing ones.
2. **Transactions:** Record retail transactions & award loyalty points.
3. **Loyalty Management:** Fetch balance, redeem points.
4. **Data Storage:** Immutable records on the blockchain.

---

## 📌 4️⃣ Features

- ✅ Immutable retail transaction recording.
- ✅ Blockchain-based loyalty points.
- ✅ Automated point awarding.
- ✅ Points redemption via API.
- ✅ Loyalty balance inquiry.
- ✅ INR ↔ Wei currency conversion.
- ✅ Smart contract management utilities.
- ✅ Dockerized deployment support.

---

## 📌 5️⃣ API Usage

**Base URL:** `http://localhost:8000`

### 🔸 API Documentation  
Available at:
- `/docs` (Swagger UI)
- `/redoc`

### 🔹 Key Endpoints & Examples:

_Check API Status_
```bash
curl -X GET "http://localhost:8000/"
```

_Record a Retail Transaction_
```bash
curl -X POST "http://localhost:8000/transactions/record" -H "Content-Type: application/json" -d '{ "customer_address": "0xCustomerEthAddress", "retailer_address": "0xRetailerEthAddress", "amount_INR": 1500.75, "product_id": "PROD123", "quantity": 2, "description": "Purchase of electronics" }'
```

_Get Transaction Details_
```bash
curl -X GET "http://localhost:8000/transactions/1"
```

_Get Loyalty Balance_
```bash
curl -X GET "http://localhost:8000/loyalty/balance/0xCustomerEthAddress"
```

_Redeem Loyalty Points_
```bash
curl -X POST "http://localhost:8000/loyalty/redeem" -H "Content-Type: application/json" -d '{ "customer_address": "0xCustomerEthAddress", "points_amount": 100 }'
```

---

## 📌 6️⃣ Local Setup

**Prerequisites:**
- Python 3.8+
- Node.js & npm (for Ganache CLI)
- Docker (optional)

**Steps:**
- Clone the repo, set environment variables, run Ganache, install dependencies, and start FastAPI.

---

## 📌 7️⃣ Deployment on Render

- Use public testnets via Infura/Alchemy.
- Secure environment configs.
- Optimize contract management for production addresses.

---

## 📌 8️⃣ Important Notes

- Replace fixed INR ↔ Wei rate with live rates.
- Ensure test ETH balance for transactions.
- Secure private keys and sensitive data.
- Improve transaction matching for production.
- Persist contract addresses after deployment.

---

## 📌 9️⃣ Scope for Future Development

- **Real-time Currency Conversion:** Use crypto APIs like CoinGecko for live conversion rates.
- **Advanced Loyalty Rules:** Introduce tier-based and bonus point systems.
- **NFT-based Loyalty:** Mint loyalty points as NFTs for tradable, unique rewards.
- **Payment Gateway Integrations:** Seamless blockchain integration with existing payment gateways.
- **Frontend Interface:** Build a modern UI for customers and retailers.
- **Event Listeners:** Automate backend updates via blockchain event subscriptions.
- **Multi-chain Compatibility:** Enable deployment across multiple blockchain networks.
- **Admin Dashboard:** Retailers can manage inventory, loyalty schemes, and analytics.
- **Decentralized Identity (DID):** Privacy-first customer authentication using decentralized IDs.
- **Off-chain Data Storage:** Use traditional databases for storing high-frequency, non-sensitive data.
