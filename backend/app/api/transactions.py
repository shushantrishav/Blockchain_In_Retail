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
        
        nonce = cs.w3.eth.get_transaction_count(cs.deployer_account.address)

        tx = cs.retail_transaction_contract.functions.recordTransaction(
            Web3.to_checksum_address(request.customer_address),
            Web3.to_checksum_address(request.retailer_address),
            amount_in_wei,
            request.product_id,
            request.quantity,
            request.description
        ).build_transaction({
            "from": cs.deployer_account.address,
            "gasPrice": cs.w3.eth.gas_price,
            "nonce": nonce,
            "chainId": cs.w3.eth.chain_id,
            "gas": 6000000 # Ensure this is sufficient
        })

        signed_tx = cs.w3.eth.account.sign_transaction(tx, private_key=cs.deployer_account.key)
        tx_hash = cs.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        
        tx_receipt = cs.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=300)

        if tx_receipt.status != 1:
            raise HTTPException(status_code=500, detail="Blockchain transaction failed.")

        # --- NEW FIX START: Extract transaction ID from event ---
        transaction_id_from_event = None
        # Get the event object from the contract instance
        # This assumes your contract has an event named 'TransactionRecorded'
        # with 'transactionId' as one of its arguments.
        event_filter = cs.retail_transaction_contract.events.TransactionRecorded.create_filter(
            fromBlock=tx_receipt.blockNumber,
            toBlock=tx_receipt.blockNumber,
            address=cs.retail_transaction_contract.address
        )
        # Process logs from the receipt to find the event
        # (This is more robust than event_filter.get_all_entries() if the event is the only one in the tx)
        processed_receipt = cs.retail_transaction_contract.events.TransactionRecorded().process_receipt(tx_receipt)

        if processed_receipt:
            # Assuming there's at least one TransactionRecorded event, get the first one
            transaction_id_from_event = processed_receipt[0]['args']['transactionId']
        else:
            # Fallback or error if event not found (e.g., contract logic changed or no event emitted)
            print("Warning: TransactionRecorded event not found in receipt. Cannot get transactionId from event.")
            # You might need to query the contract directly if no event is found or handle this case
            # For now, let's raise an error as we expect the event to be there.
            raise HTTPException(status_code=500, detail="Transaction ID not found in blockchain event.")
        
        # Now use the ID obtained from the event
        txn_details = cs.retail_transaction_contract.functions.getTransaction(transaction_id_from_event).call()
        # --- NEW FIX END ---

        loyalty_points_award_result = await award_loyalty_points(
            request.customer_address,
            amount_in_wei,
            cs.deployer_account
        )
        loyalty_points_awarded = loyalty_points_award_result.get("points_awarded", 0)

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
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error recording transaction: {e}")

# ... (rest of the router functions remain the same) ...

@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_retail_transaction(transaction_id: int):
    if not cs.retail_transaction_contract:
        raise HTTPException(status_code=500, detail="Retail Transaction contract not initialized.")

    try:
        txn_details = cs.retail_transaction_contract.functions.getTransaction(transaction_id).call()
        if txn_details[0] == 0: # Assuming 0 indicates not found
            raise HTTPException(status_code=404, detail="Transaction not found.")

        # You need to determine how to get loyalty_points_awarded for an existing transaction.
        # If it's stored in the smart contract's transaction details, use its index.
        # If it needs to be calculated or retrieved from another source, add that logic here.
        # For demonstration, let's assume it's the 8th element if your contract returns it.
        # If not, you might need to query your loyalty contract or store it with the transaction.
        # For now, I'll put a placeholder or a default value if it's not directly in txn_details.

        # *** IMPORTANT: Replace `txn_details[8]` with the actual index if loyalty points are returned,
        # or implement logic to fetch them if they're not part of getTransaction() directly. ***
        # If your getTransaction does NOT return loyalty_points_awarded, you might have to query
        # your loyalty contract for the customer's balance or rethink how this field is populated
        # when fetching a historical transaction.
        
        # Placeholder for loyalty_points_awarded if not directly in txn_details, adjust as needed:
        # For now, setting to 0 or a sensible default if it's not directly part of the fetched txn_details
        # If your contract's getTransaction function truly does not return this, you'll need a different approach.
        default_loyalty_points_awarded = 0 # Or fetch from loyalty contract if possible

        # If txn_details has loyalty points awarded at a specific index, use that:
        # For example, if it's txn_details[8] after description, use it:
        # loyalty_points = txn_details[8] if len(txn_details) > 8 else default_loyalty_points_awarded

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
            transaction_hash="", # This won't be available directly when fetching by ID
            # --- FIX: Add loyalty_points_awarded here ---
            loyalty_points_awarded=default_loyalty_points_awarded # Or the actual value from txn_details if available
            # e.g., loyalty_points_awarded=txn_details[8] if your smart contract getTransaction returns it
        )

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error fetching transaction: {e}")