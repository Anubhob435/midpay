# MidPay API Documentation

## Base URL
`http://localhost:5000/api`

## Authentication
All API endpoints require an API key to be included in the request header:

```
X-API-Key: your-api-key-here
```

To get an API key, use the `generate_api_key.py` script. The key will be stored in `validkeys.json`.

## Endpoints

### Get Account Balance
**GET** `/balance/{user}`

*Get the balance of a specific user account*

**Parameters:**
- `user`: User ID (A or B)

**Response:**
```json
{
  "status": "success",
  "balance": 1000.0
}
```

### Get All Accounts
**GET** `/accounts`

*Get balances for all accounts including escrow*

**Response:**
```json
{
  "status": "success",
  "accounts": {
    "A": 90.0,
    "B": 1400.0,
    "escrow": 510.0
  }
}
```

### Create Transaction
**POST** `/transactions`

*Create a new transaction from A to escrow*

**Request Body:**
```json
{
  "amount": 100.0,
  "description": "Web development services"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Payment of $100.0 moved to escrow. Transaction ID: 1234567890",
  "transaction_id": "1234567890"
}
```

### Mark Transaction as Completed
**PUT** `/transactions/{transaction_id}/complete`

*B marks a service as completed*

**Parameters:**
- `transaction_id`: ID of the transaction to mark as completed

**Response:**
```json
{
  "status": "success",
  "message": "Service marked as completed. Waiting for confirmation from A."
}
```

### Confirm Transaction Completion
**PUT** `/transactions/{transaction_id}/confirm`

*A confirms completion and releases payment to B*

**Parameters:**
- `transaction_id`: ID of the transaction to confirm

**Response:**
```json
{
  "status": "success",
  "message": "Payment of $100.0 released to B."
}
```

### Cancel Transaction
**PUT** `/transactions/{transaction_id}/cancel`

*A cancels a transaction and returns funds from escrow*

**Parameters:**
- `transaction_id`: ID of the transaction to cancel

**Response:**
```json
{
  "status": "success",
  "message": "Transaction cancelled. $100.0 returned to A."
}
```

### Get Transaction Status
**GET** `/transactions/{transaction_id}`

*Get detailed status of a specific transaction*

**Parameters:**
- `transaction_id`: ID of the transaction to retrieve

**Response:**
```json
{
  "status": "success",
  "transaction": {
    "amount": 100.0,
    "service": "Web development services",
    "status": "pending",
    "created_at": "2025-03-27 17:56:13",
    "completed_at": null,
    "released_at": null,
    "blockchain_status": "verified",
    "blockchain_history": [
      {
        "transaction_id": "1234567890",
        "amount": 100.0,
        "service": "Web development services",
        "status": "pending",
        "created_at": "2025-03-27 17:56:13",
        "from": "A",
        "to": "escrow",
        "signature": "..."
      }
    ]
  }
}
```

### Verify Blockchain
**GET** `/blockchain/verify`

*Verify the integrity of the blockchain*

**Response:**
```json
{
  "status": "success",
  "message": "Blockchain is valid"
}
```

## New Features

### Get Transaction History
**GET** `/transactions/history`

*Get filtered transaction history*

**Query Parameters:**
- `user` (optional): Filter by user (A or B)
- `status` (optional): Filter by transaction status
- `start_date` (optional): Filter by transactions after this date (format: YYYY-MM-DD)
- `end_date` (optional): Filter by transactions before this date (format: YYYY-MM-DD)

**Response:**
```json
{
  "status": "success",
  "transactions": {
    "1234567890": {
      "amount": 100.0,
      "service": "Web development services",
      "status": "completed",
      "created_at": "2025-03-27 17:56:13",
      "completed_at": "2025-03-27 18:30:45",
      "released_at": null
    },
    "9876543210": {
      "amount": 200.0,
      "service": "Logo design",
      "status": "released",
      "created_at": "2025-03-28 10:12:33",
      "completed_at": "2025-03-28 14:25:10",
      "released_at": "2025-03-29 09:15:22"
    }
  }
}
```

### Create Batch Transactions
**POST** `/transactions/batch`

*Create multiple transactions at once*

**Request Body:**
```json
{
  "transactions": [
    {
      "amount": 50.0,
      "description": "Website maintenance"
    },
    {
      "amount": 75.0,
      "description": "Content writing"
    }
  ]
}
```

**Response:**
```json
{
  "status": "success",
  "results": [
    {
      "status": "success", 
      "message": "Payment of $50.0 moved to escrow. Transaction ID: 1234567891",
      "transaction_id": "1234567891"
    },
    {
      "status": "success", 
      "message": "Payment of $75.0 moved to escrow. Transaction ID: 1234567892",
      "transaction_id": "1234567892"
    }
  ]
}
```

### Create User
**POST** `/users`

*Create a new user with an initial balance*

**Request Body:**
```json
{
  "user_id": "C",
  "initial_balance": 500.0
}
```

**Response:**
```json
{
  "status": "success",
  "message": "User C created with initial balance of $500.0"
}
```

### Get User Details
**GET** `/users/{user_id}`

*Get detailed information about a user*

**Parameters:**
- `user_id`: ID of the user to retrieve

**Response:**
```json
{
  "status": "success",
  "user": {
    "user_id": "C",
    "balance": 500.0,
    "transaction_count": 5,
    "transaction_history": [
      {
        "amount": -100.0,
        "description": "Payment to escrow for Web design [ID: 1234567893]",
        "timestamp": "2025-03-30 08:45:12"
      },
      {
        "amount": 200.0,
        "description": "Payment received for Logo design [ID: 1234567894]",
        "timestamp": "2025-03-31 14:20:36"
      }
    ]
  }
}
```

### Create Dispute
**POST** `/transactions/{transaction_id}/dispute`

*Create a dispute for a transaction*

**Parameters:**
- `transaction_id`: ID of the transaction to dispute

**Request Body:**
```json
{
  "reason": "Service not delivered as described"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Dispute created with ID: D-1234567890-1586432109",
  "dispute_id": "D-1234567890-1586432109"
}
```

### Resolve Dispute
**PUT** `/disputes/{dispute_id}/resolve`

*Resolve a dispute by refunding or releasing payment*

**Parameters:**
- `dispute_id`: ID of the dispute to resolve

**Request Body:**
```json
{
  "resolution": "refund"  // or "release"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Dispute resolved with resolution: refund"
}
```

### Create Multi-Party Transaction
**POST** `/transactions/multi`

*Create a transaction involving multiple parties*

**Request Body:**
```json
{
  "parties": ["A", "C", "B"],  // Last party is the receiver
  "amount": 300.0,
  "description": "Joint project payment"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Multi-party payment of $300.0 moved to escrow. Transaction ID: MULTI-1586432110",
  "transaction_id": "MULTI-1586432110"
}
```

### List API Keys
**GET** `/keys`

*List all active API keys (masked for security)*

**Response:**
```json
{
  "status": "success",
  "keys": {
    "count": 2,
    "keys": ["****abcdef", "****123456"]
  }
}
```

### Revoke API Key
**POST** `/keys/revoke`

*Revoke an API key*

**Request Body:**
```json
{
  "key": "api-key-to-revoke"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "API key revoked successfully"
}
```

### Schedule Transaction
**POST** `/transactions/scheduled`

*Schedule a transaction for future execution*

**Request Body:**
```json
{
  "amount": 150.0,
  "description": "Monthly service fee",
  "execute_at": "2025-05-01 00:00:00"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Transaction scheduled for 2025-05-01 00:00:00. Transaction ID: SCHEDULED-1586432111",
  "transaction_id": "SCHEDULED-1586432111"
}
```

### Get Transaction Volume Analytics
**GET** `/analytics/volume`

*Get transaction volume analytics for a specific time period*

**Query Parameters:**
- `period` (optional): Time period (default: "month", options: "day", "week", "month", "year")

**Response:**
```json
{
  "status": "success",
  "period": "month",
  "total_volume": 1250.0,
  "transaction_count": 8,
  "status_breakdown": {
    "pending": 2,
    "completed": 3,
    "released": 2,
    "cancelled": 1,
    "disputed": 0,
    "scheduled": 0
  }
}
```

### Get User Analytics
**GET** `/analytics/user/{user_id}`

*Get detailed analytics for a specific user*

**Parameters:**
- `user_id`: ID of the user to analyze

**Response:**
```json
{
  "status": "success",
  "user_id": "A",
  "current_balance": 750.0,
  "total_incoming": 800.0,
  "total_outgoing": 1050.0,
  "transaction_count": 12,
  "blockchain_transaction_count": 24
}
```

## Error Responses

When an error occurs, the API will respond with an appropriate HTTP status code and a JSON object:

```json
{
  "status": "failed",
  "message": "Error message describing the issue"
}
```

Common error status codes:
- `400 Bad Request`: Invalid parameters or request body
- `404 Not Found`: Resource not found
- `401 Unauthorized`: Invalid or missing API key

## Implementation Notes

This API is built with Flask and interfaces with the MidPay system which uses blockchain technology to record all transactions. Each transaction is signed with digital signatures and stored in an immutable blockchain ledger.