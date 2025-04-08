from flask import Flask, request, jsonify
from flask_cors import CORS
from midpay import MidPay
import json
from functools import wraps

app = Flask(__name__)
CORS(app)  # Enable cross-origin requests

# Initialize MidPay instance
midpay = MidPay()

def validate_api_key():
    """Validate the API key from the request header"""
    api_key = request.headers.get('X-API-Key')
    if not api_key:
        return False
    
    try:
        with open('validkeys.json', 'r') as file:
            valid_keys = json.load(file)
            return api_key in valid_keys
    except:
        return False

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not validate_api_key():
            return jsonify({"status": "failed", "message": "Invalid or missing API key"}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/api/balance/<user>', methods=['GET'])
@require_api_key
def get_balance(user):
    if user not in ['A', 'B']:
        return jsonify({"status": "failed", "message": "Invalid user ID"}), 400
    
    balance = midpay.get_balance(user)
    return jsonify({"status": "success", "balance": balance})

@app.route('/api/accounts', methods=['GET'])
@require_api_key
def get_accounts():
    a_balance = midpay.get_balance("A")
    b_balance = midpay.get_balance("B")
    
    return jsonify({
        "status": "success",
        "accounts": {
            "A": a_balance,
            "B": b_balance,
            "escrow": midpay.escrow_account
        }
    })

@app.route('/api/transactions', methods=['POST'])
@require_api_key
def create_transaction():
    data = request.json
    
    if not data or 'amount' not in data or 'description' not in data:
        return jsonify({"status": "failed", "message": "Missing required fields"}), 400
    
    result = midpay.create_transaction(float(data['amount']), data['description'])
    return jsonify(result)

@app.route('/api/transactions/<transaction_id>/complete', methods=['PUT'])
@require_api_key
def mark_completed(transaction_id):
    result = midpay.mark_service_completed(transaction_id)
    return jsonify(result)

@app.route('/api/transactions/<transaction_id>/confirm', methods=['PUT'])
@require_api_key
def confirm_transaction(transaction_id):
    result = midpay.confirm_completion(transaction_id)
    return jsonify(result)

@app.route('/api/transactions/<transaction_id>/cancel', methods=['PUT'])
@require_api_key
def cancel_transaction(transaction_id):
    result = midpay.cancel_transaction(transaction_id)
    return jsonify(result)

@app.route('/api/transactions/<transaction_id>', methods=['GET'])
@require_api_key
def get_transaction(transaction_id):
    result = midpay.get_transaction_status(transaction_id)
    return jsonify(result)

@app.route('/api/blockchain/verify', methods=['GET'])
@require_api_key
def verify_blockchain():
    result = midpay.verify_blockchain()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')