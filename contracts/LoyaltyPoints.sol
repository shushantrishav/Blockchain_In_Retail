// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title LoyaltyPoints
 * @dev A smart contract to manage loyalty points for customers.
 * Each customer's loyalty points are mapped to their Ethereum address.
 */
contract LoyaltyPoints {
    // Mapping to store loyalty points balance for each address
    mapping(address => uint256) private loyaltyBalances;

    // Event emitted when loyalty points are awarded to an address
    event PointsAwarded(address indexed recipient, uint256 amount);

    // Event emitted when loyalty points are redeemed by an address
    event PointsRedeemed(address indexed redeemer, uint256 amount);

    /**
     * @dev Awards loyalty points to a specific address.
     * @param _recipient The address to whom points are to be awarded.
     * @param _amount The number of loyalty points to award.
     */
    function awardPoints(address _recipient, uint256 _amount) public {
        // Ensure a valid recipient address
        require(_recipient != address(0), "Invalid recipient address.");
        // Ensure a positive amount of points
        require(_amount > 0, "Amount of points must be positive.");

        loyaltyBalances[_recipient] += _amount; // Add points to the recipient's balance
        emit PointsAwarded(_recipient, _amount); // Emit an event
    }

    /**
     * @dev Redeems loyalty points from a specific address.
     * Points can only be redeemed if the recipient has sufficient balance.
     * @param _redeemer The address from whom points are to be redeemed.
     * @param _amount The number of loyalty points to redeem.
     */
    function redeemPoints(address _redeemer, uint256 _amount) public {
        // Ensure a valid redeemer address
        require(_redeemer != address(0), "Invalid redeemer address.");
        // Ensure a positive amount of points
        require(_amount > 0, "Amount of points must be positive.");
        // Ensure the redeemer has sufficient balance
        require(loyaltyBalances[_redeemer] >= _amount, "Insufficient loyalty points.");

        loyaltyBalances[_redeemer] -= _amount; // Subtract points from the redeemer's balance
        emit PointsRedeemed(_redeemer, _amount); // Emit an event
    }

    /**
     * @dev Retrieves the current loyalty points balance for a specific address.
     * @param _owner The address whose balance is to be queried.
     * @return The current loyalty points balance of the owner.
     */
    function getBalance(address _owner) public view returns (uint256) {
        // Ensure a valid owner address
        require(_owner != address(0), "Invalid owner address.");
        return loyaltyBalances[_owner]; // Return the balance
    }
}

