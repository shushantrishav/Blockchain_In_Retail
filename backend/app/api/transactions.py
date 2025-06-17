from fastapi import APIRouter, HTTPException
from web3 import Web3

from app.startup import contractsStartup as cs
from app.models.schemas import RecordTransactionRequest, TransactionResponse
from app.services.currencyManager.currency_converter import INR_to_wei, wei_to_INR
from app.services.loyaltyManager.loyalty_util import award_loyalty_points

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.post("/record", response_model=TransactionResponse)
async def record_retail_transaction(request: RecordTransactionRequest):
    if not cs.retail_transaction_contract or not cs.loyalty_points_contract or not cs.deployer_account:
        raise HTTPException(status_code=500, detail="Contracts not initialized.")

    try:
        amount_in_wei = INR_to_wei(request.amount_INR)
        nonce = cs.w3.eth.get_transaction_count(cs.deployer_account)

        tx = cs.retail_transaction_contract.functions.recordTransaction(
            Web3.to_checksum_address(request.customer_address),
            Web3.to_checksum_address(request.retailer_address),
            amount_in_wei,
            request.product_id,
            request.quantity,
            request.description
        ).build_transaction({
            "from": cs.deployer_account,
            "gasPrice": cs.w3.eth.gas_price,
            "nonce": nonce,
            "chainId": cs.w3.eth.chain_id
        })

        tx_hash = cs.w3.eth.send_transaction(tx)
        tx_receipt = cs.w3.eth.wait_for_transaction_receipt(tx_hash)

        if tx_receipt.status != 1:
            raise HTTPException(status_code=500, detail="Transaction failed on blockchain.")

        transaction_id = 0
        for log in tx_receipt.logs:
            try:
                event_data = cs.retail_transaction_contract.events.TransactionRecorded().process_receipt(tx_receipt)
                if event_data:
                    transaction_id = event_data[0]['args']['transactionId']
                    break
            except:
                pass

        if transaction_id == 0:
            total_transactions = cs.retail_transaction_contract.functions.getTotalTransactions().call()
            transaction_id = total_transactions

        loyalty_award_result = await award_loyalty_points(
            request.customer_address,
            amount_in_wei,
            cs.deployer_account
        )

        loyalty_points_awarded = loyalty_award_result.get("points_awarded", 0)

        txn_details = cs.retail_transaction_contract.functions.getTransaction(transaction_id).call()

        return TransactionResponse(
            transaction_id=txn_details[0],
            customer_address=txn_details[1],
            retailer_address=txn_details[2],
            amount_INR=wei_to_INR(txn_details[3]),
            amount_wei=txn_details[3],
            product_id=txn_details[4],
            quantity=txn_details[5],
            timestamp=txn_details[6],
            description=txn_details[7],
            transaction_hash=tx_hash.hex(),
            loyalty_points_awarded=loyalty_points_awarded
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error recording transaction: {e}")

@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_retail_transaction(transaction_id: int):
    if not cs.retail_transaction_contract:
        raise HTTPException(status_code=500, detail="Retail Transaction contract not initialized.")

    try:
        txn_details = cs.retail_transaction_contract.functions.getTransaction(transaction_id).call()
        if txn_details[0] == 0:
            raise HTTPException(status_code=404, detail="Transaction not found.")

        return TransactionResponse(
            transaction_id=txn_details[0],
            customer_address=txn_details[1],
            retailer_address=txn_details[2],
            amount_INR=wei_to_INR(txn_details[3]),
            amount_wei=txn_details[3],
            product_id=txn_details[4],
            quantity=txn_details[5],
            timestamp=txn_details[6],
            description=txn_details[7],
            transaction_hash=""
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching transaction: {e}")
