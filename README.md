# MidPay

MidPay is a simulation of an escrow payment system that facilitates secure transactions between two parties (A and B). It ensures that payments are held in escrow until services are completed and confirmed, now enhanced with blockchain technology and a REST API.

## Features

- **Blockchain Integration**: Immutable transaction records using proof-of-work
- **Digital Signatures**: RSA-based cryptographic verification of transactions
- **Escrow Payments**: Secure fund transfers with an escrow holding system
- **Transaction Management**: Create, complete, confirm, and cancel transactions
- **Account Tracking**: Monitor balances for both parties and the escrow account
- **Transaction History**: Blockchain-verified transaction history
- **REST API**: HTTP interface for integrating with web and mobile applications

## Blockchain Implementation

- **Proof of Work**: Simple mining algorithm with adjustable difficulty
- **Chain Validation**: Ensures blockchain integrity through hash verification
- **Digital Signatures**: RSA-2048 cryptographic signatures for transaction security
- **Transaction History**: Immutable record of all activities stored in blocks

## Getting Started

### Prerequisites

- Python 3.6 or higher
- Required packages: cryptography, flask, flask-cors

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/midpay.git
   cd midpay
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application (choose one method):

   **CLI Mode**:
   ```
   python midpay.py
   ```

   **API Server Mode**:
   ```
   python api.py
   ```

## CLI Mode Usage

The simulation offers a menu-driven interface with the following options:

1. View Account Balances
2. Create New Transaction (as A)
3. Mark Service as Completed (as B)
4. Confirm and Release Payment (as A)
5. Cancel Transaction (as A)
6. Check Transaction Status
7. Verify Blockchain Integrity
8. Exit

## API Mode Usage

Start the API server with `python api.py` and access it at `http://localhost:5000/api`.

### Example API Requests

**1. Create a new transaction:**
```bash
curl -X POST http://localhost:5000/api/transactions \
  -H "Content-Type: application/json" \
  -d '{"amount": 50.0, "description": "Logo design"}'
```

**2. Check transaction status:**
```bash
curl http://localhost:5000/api/transactions/1743078373
```

**3. Mark transaction as completed:**
```bash
curl -X PUT http://localhost:5000/api/transactions/1743078373/complete
```

See [API_DOCS.md](API_DOCS.md) for complete API documentation.

## File Structure

- `midpay.py`: Main application with the MidPay class and CLI interface
- `blockchain.py`: Blockchain implementation with digital signatures
- `api.py`: REST API implementation using Flask
- `requirements.txt`: Dependencies for the project
- `A_bank.json`: Stores Party A's account balance and transaction history
- `B_bank.json`: Stores Party B's account balance and transaction history
- `API_DOCS.md`: Complete API documentation

## System Architecture

MidPay consists of several components working together:

1. **Core Business Logic** (`midpay.py`):
   - Manages transaction flow and account ledgers
   - Provides the main MidPay class used by both CLI and API

2. **Blockchain System** (`blockchain.py`):
   - Implements blocks and chain with proof-of-work
   - Handles digital signatures for transaction verification
   - Provides immutable transaction history

3. **REST API** (`api.py`):
   - Exposes system functionality via HTTP endpoints
   - Enables integration with external applications

## Security Notes

This is a simulation only and not designed for real-world financial transactions. While it demonstrates blockchain concepts, a production system would require more robust security measures including:

- User authentication and authorization
- Secure key storage
- Network communication encryption
- Additional validation and security checks

## License

[MIT License](LICENSE)
