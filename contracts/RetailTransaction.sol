// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title RetailTransaction
 * @dev A smart contract to record and manage retail transactions on the blockchain.
 */
contract RetailTransaction {
    // Structure to hold details of a single transaction
    struct Transaction {
        uint256 transactionId;     // Unique identifier for the transaction
        address customerAddress;   // Address of the customer
        address retailerAddress;   // Address of the retailer
        uint256 amountInWei;       // Transaction amount in Wei (smallest unit of Ether)
        string productId;          // Identifier for the product purchased
        uint256 quantity;          // Quantity of the product
        uint256 timestamp;         // Timestamp when the transaction was recorded
        string description;        // Optional description of the transaction
    }

    // Mapping to store transactions by their unique ID
    mapping(uint256 => Transaction) public transactions;

    // Counter for generating unique transaction IDs
    uint256 private nextTransactionId;

    // Event emitted when a new transaction is successfully recorded
    event TransactionRecorded(
        uint256 indexed transactionId,
        address indexed customer,
        address indexed retailer,
        uint256 amountInWei,
        string productId,
        uint256 quantity,
        uint256 timestamp
    );

    /**
     * @dev Constructor of the contract. Initializes the transaction ID counter.
     */
    constructor() {
        nextTransactionId = 1; // Start transaction IDs from 1
    }

    /**
     * @dev Records a new retail transaction.
     * @param _customerAddress The address of the customer.
     * @param _retailerAddress The address of the retailer.
     * @param _amountInWei The total amount of the transaction in Wei.
     * @param _productId The identifier of the product.
     * @param _quantity The quantity of the product purchased.
     * @param _description An optional description for the transaction.
     * @return The unique transaction ID generated for this transaction.
     */
    function recordTransaction(
        address _customerAddress,
        address _retailerAddress,
        uint256 _amountInWei,
        string memory _productId,
        uint256 _quantity,
        string memory _description
    ) public returns (uint256) {
        // Ensure that the amount is positive
        require(_amountInWei > 0, "Transaction amount must be positive.");
        // Ensure that the quantity is positive
        require(_quantity > 0, "Quantity must be positive.");
        // Ensure valid addresses are provided
        require(_customerAddress != address(0), "Invalid customer address.");
        require(_retailerAddress != address(0), "Invalid retailer address.");

        uint256 currentTransactionId = nextTransactionId;

        // Store the transaction details
        transactions[currentTransactionId] = Transaction({
            transactionId: currentTransactionId,
            customerAddress: _customerAddress,
            retailerAddress: _retailerAddress,
            amountInWei: _amountInWei,
            productId: _productId,
            quantity: _quantity,
            timestamp: block.timestamp,
            description: _description
        });

        // Increment the next transaction ID for future use
        nextTransactionId++;

        // Emit an event to log the transaction
        emit TransactionRecorded(
            currentTransactionId,
            _customerAddress,
            _retailerAddress,
            _amountInWei,
            _productId,
            _quantity,
            block.timestamp
        );

        return currentTransactionId;
    }

    /**
     * @dev Retrieves the details of a specific transaction by its ID.
     * @param _transactionId The ID of the transaction to retrieve.
     * @return transactionId The unique ID of the transaction.
     * @return customerAddress The address of the customer.
     * @return retailerAddress The address of the retailer.
     * @return amountInWei The total amount of the transaction in Wei.
     * @return productId The identifier of the product.
     * @return quantity The quantity of the product purchased.
     * @return timestamp The timestamp when the transaction was recorded.
     * @return description The description of the transaction.
     */
    function getTransaction(uint256 _transactionId)
        public
        view
        returns (
            uint256 transactionId,
            address customerAddress,
            address retailerAddress,
            uint256 amountInWei,
            string memory productId,
            uint256 quantity,
            uint256 timestamp,
            string memory description
        )
    {
        // Ensure the transaction ID is valid
        require(_transactionId > 0 && _transactionId < nextTransactionId, "Invalid transaction ID.");

        Transaction storage txn = transactions[_transactionId];
        return (
            txn.transactionId,
            txn.customerAddress,
            txn.retailerAddress,
            txn.amountInWei,
            txn.productId,
            txn.quantity,
            txn.timestamp,
            txn.description
        );
    }

    /**
     * @dev Returns the total number of transactions recorded so far.
     * @return The current value of nextTransactionId, which represents the total count + 1.
     */
    function getTotalTransactions() public view returns (uint256) {
        return nextTransactionId - 1; // Subtract 1 as nextTransactionId is the next available ID
    }
}

