Collecting workspace information# MidPay API Documentation

## Base URL
`http://localhost:5000/api`

## Authentication
This API currently does not require authentication.

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

## Implementation Notes

This API is built with Flask and interfaces with the MidPay system which uses blockchain technology to record all transactions. Each transaction is signed with digital signatures and stored in an immutable blockchain ledger.