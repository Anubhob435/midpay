# MidPay

MidPay is a simulation of an escrow payment system that facilitates secure transactions between two parties (A and B). It ensures that payments are held in escrow until services are completed and confirmed, now enhanced with blockchain technology.

## Features

- **Blockchain Integration**: Immutable transaction records
- **Digital Signatures**: Cryptographic verification of transactions
- **Escrow Payments**: Secure fund transfers with an escrow holding system
- **Transaction Management**: Create, complete, confirm, and cancel transactions
- **Account Tracking**: Monitor balances for both parties and the escrow account
- **Transaction History**: Blockchain-verified transaction history

## Blockchain Implementation

- **Proof of Work**: Simple mining algorithm
- **Chain Validation**: Ensures blockchain integrity
- **Digital Signatures**: RSA-based cryptographic signatures
- **Transaction History**: Immutable record of all activities

## Getting Started

### Prerequisites

- Python 3.6 or higher
- Required packages: hashlib, cryptography

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

3. Run the simulation:
   ```
   python midpay.py
   ```

## Usage

The simulation offers a menu-driven interface with the following options:

1. View Account Balances
2. Create New Transaction (as A)
3. Mark Service as Completed (as B)
4. Confirm and Release Payment (as A)
5. Cancel Transaction (as A)
6. Check Transaction Status
7. Verify Blockchain Integrity
8. Exit

## File Structure

- `midpay.py`: Main application with the MidPay class and simulation logic
- `blockchain.py`: Blockchain implementation for transaction verification
- `A_bank.json`: Stores Party A's account balance and transaction history
- `B_bank.json`: Stores Party B's account balance and transaction history

## Security Notes

This is a simulation only and not designed for real-world financial transactions. While it demonstrates blockchain concepts, a production system would require more robust security measures.

## License

[MIT License](LICENSE)
