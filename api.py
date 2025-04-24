from flask import Flask, request, jsonify
from flask_cors import CORS
from midpay import MidPay
import json
from functools import wraps
from datetime import datetime, timedelta

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

# New API endpoints for enhanced features

@app.route('/api/transactions/history', methods=['GET'])
@require_api_key
def get_transaction_history():
    user = request.args.get('user')
    status = request.args.get('status')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    result = midpay.get_transaction_history(user, status, start_date, end_date)
    return jsonify(result)

@app.route('/api/transactions/batch', methods=['POST'])
@require_api_key
def create_batch_transaction():
    data = request.json
    
    if not data or 'transactions' not in data:
        return jsonify({"status": "failed", "message": "Missing transactions array"}), 400
    
    results = []
    for tx in data['transactions']:
        if 'amount' in tx and 'description' in tx:
            result = midpay.create_transaction(float(tx['amount']), tx['description'])
            results.append(result)
    
    return jsonify({"status": "success", "results": results})

@app.route('/api/users', methods=['POST'])
@require_api_key
def create_user():
    data = request.json
    if not data or 'user_id' not in data or 'initial_balance' not in data:
        return jsonify({"status": "failed", "message": "Missing required fields"}), 400
    
    result = midpay.create_user(data['user_id'], float(data['initial_balance']))
    return jsonify(result)

@app.route('/api/users/<user_id>', methods=['GET'])
@require_api_key
def get_user(user_id):
    result = midpay.get_user_details(user_id)
    return jsonify(result)

@app.route('/api/transactions/<transaction_id>/dispute', methods=['POST'])
@require_api_key
def create_dispute(transaction_id):
    data = request.json
    if not data or 'reason' not in data:
        return jsonify({"status": "failed", "message": "Missing reason for dispute"}), 400
    
    result = midpay.create_dispute(transaction_id, data['reason'])
    return jsonify(result)

@app.route('/api/disputes/<dispute_id>/resolve', methods=['PUT'])
@require_api_key
def resolve_dispute(dispute_id):
    data = request.json
    if not data or 'resolution' not in data:
        return jsonify({"status": "failed", "message": "Missing resolution decision"}), 400
    
    result = midpay.resolve_dispute(dispute_id, data['resolution'])
    return jsonify(result)

@app.route('/api/transactions/multi', methods=['POST'])
@require_api_key
def create_multi_party_transaction():
    data = request.json
    if not data or 'parties' not in data or 'amount' not in data or 'description' not in data:
        return jsonify({"status": "failed", "message": "Missing required fields"}), 400
    
    result = midpay.create_multi_party_transaction(data['parties'], float(data['amount']), data['description'])
    return jsonify(result)

@app.route('/api/keys', methods=['GET'])
@require_api_key
def list_api_keys():
    return jsonify({"status": "success", "keys": midpay.get_api_keys()})

@app.route('/api/keys/revoke', methods=['POST'])
@require_api_key
def revoke_api_key():
    data = request.json
    if not data or 'key' not in data:
        return jsonify({"status": "failed", "message": "Missing key to revoke"}), 400
    
    result = midpay.revoke_api_key(data['key'])
    return jsonify(result)

@app.route('/api/transactions/scheduled', methods=['POST'])
@require_api_key
def schedule_transaction():
    data = request.json
    if not data or 'amount' not in data or 'description' not in data or 'execute_at' not in data:
        return jsonify({"status": "failed", "message": "Missing required fields"}), 400
    
    result = midpay.schedule_transaction(float(data['amount']), data['description'], data['execute_at'])
    return jsonify(result)

@app.route('/api/analytics/volume', methods=['GET'])
@require_api_key
def get_transaction_volume():
    period = request.args.get('period', 'month')
    result = midpay.get_transaction_volume(period)
    return jsonify(result)

@app.route('/api/analytics/user/<user_id>', methods=['GET'])
@require_api_key
def get_user_analytics(user_id):
    result = midpay.get_user_analytics(user_id)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')