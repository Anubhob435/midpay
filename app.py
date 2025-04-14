from flask import Flask, render_template, request, redirect, url_for, flash, session
from midpay import MidPay
import secrets
import json
import os
import hashlib  # For password hashing in the future
from generate_api_key import generate_api_key, save_api_key  # Import API key generation functions

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Initialize MidPay instance
midpay = MidPay()

def load_users():
    """Load user data from users.json"""
    try:
        with open('users.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Return empty user list if file doesn't exist or is invalid
        return {"users": []}

def save_users(user_data):
    """Save user data to users.json"""
    with open('users.json', 'w') as f:
        json.dump(user_data, f, indent=2)

@app.route('/')
def index():
    # Get account balances
    a_balance = midpay.get_balance("A")
    b_balance = midpay.get_balance("B")
    escrow_balance = midpay.escrow_account
    
    # Get recent transactions (only if user is logged in)
    recent_transactions = []
    if 'username' in session:
        for tx_id in midpay.transactions:
            tx_info = midpay.get_transaction_status(tx_id)
            if tx_info["status"] == "success":
                tx_data = tx_info["transaction"]
                tx_data["id"] = tx_id  # Add transaction ID to the data
                recent_transactions.append(tx_data)
        
        # Reverse to show newest first
        recent_transactions.reverse()
    
    # Always render index.html, but with limited data for non-logged in users
    return render_template('index.html', 
                          a_balance=a_balance, 
                          b_balance=b_balance, 
                          escrow_balance=escrow_balance, 
                          transactions=recent_transactions[:5],  # Show only the 5 most recent transactions
                          username=session.get('username', ''),
                          name=session.get('name', ''),
                          user_role=session.get('user_role', ''))

@app.route('/dashboard')
def dashboard():
    # Redirect to login if not logged in
    if 'username' not in session:
        flash('Please login to view your dashboard', 'info')
        return redirect(url_for('login_page'))
        
    # Get account balances
    a_balance = midpay.get_balance("A")
    b_balance = midpay.get_balance("B")
    escrow_balance = midpay.escrow_account
    
    # Get recent transactions
    recent_transactions = []
    for tx_id in midpay.transactions:
        tx_info = midpay.get_transaction_status(tx_id)
        if tx_info["status"] == "success":
            tx_data = tx_info["transaction"]
            tx_data["id"] = tx_id  # Add transaction ID to the data
            recent_transactions.append(tx_data)
    
    # Reverse to show newest first
    recent_transactions.reverse()
    
    return render_template('index.html', 
                           a_balance=a_balance, 
                           b_balance=b_balance, 
                           escrow_balance=escrow_balance, 
                           transactions=recent_transactions[:5],  # Show only the 5 most recent transactions
                           username=session.get('username', ''),
                           name=session.get('name', ''),
                           user_role=session.get('user_role', ''),
                           show_dashboard=True)

@app.route('/login_page')
def login_page():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not username or not password:
        flash('Please provide both username and password', 'error')
        return redirect(url_for('login_page'))
    
    # Load users from JSON file
    user_data = load_users()
    
    # Find the user
    user = next((u for u in user_data['users'] if u['username'] == username), None)
    
    if user and user['password'] == password:  # In production, use proper password hashing
        # Store user info in session
        session['username'] = user['username']
        session['user_role'] = user['role']
        session['name'] = user['name']
        session['email'] = user['email']
        
        flash(f'Welcome back, {user["name"]}!', 'success')
        return redirect(url_for('dashboard'))
    else:
        flash('Invalid username or password', 'error')
        return redirect(url_for('login_page'))

@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

@app.route('/register_page')
def register_page():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    role = request.form.get('role')
    email = request.form.get('email')
    name = request.form.get('name')
    
    # Basic validation
    if not all([username, password, confirm_password, role, email, name]):
        flash('All fields are required', 'error')
        return redirect(url_for('register_page'))
    
    if password != confirm_password:
        flash('Passwords do not match', 'error')
        return redirect(url_for('register_page'))
    
    if role not in ['A', 'B']:
        flash('Invalid role selected', 'error')
        return redirect(url_for('register_page'))
    
    # Load existing users
    user_data = load_users()
    
    # Check if username already exists
    if any(u['username'] == username for u in user_data['users']):
        flash('Username already exists', 'error')
        return redirect(url_for('register_page'))
    
    # Add the new user
    new_user = {
        'username': username,
        'password': password,  # In production, use proper password hashing
        'role': role,
        'email': email,
        'name': name
    }
    
    user_data['users'].append(new_user)
    
    # Save updated user data
    save_users(user_data)
    
    flash('Registration successful! You can now login.', 'success')
    return redirect(url_for('login_page'))

@app.route('/create_transaction', methods=['POST'])
def create_transaction():
    # Check if user is logged in
    if 'username' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login_page'))
        
    amount = request.form.get('amount')
    description = request.form.get('description')
    
    if not amount or not description:
        flash('Please provide both amount and description', 'error')
        return redirect(url_for('index'))
    
    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Amount must be positive")
            
        result = midpay.create_transaction(amount, description)
        
        if result["status"] == "success":
            flash(f'Transaction created successfully! ID: {result["transaction_id"]}', 'success')
        else:
            flash(f'Error: {result["message"]}', 'error')
            
    except ValueError as e:
        flash(f'Invalid amount: {str(e)}', 'error')
    
    return redirect(url_for('index'))

@app.route('/mark_completed/<transaction_id>', methods=['POST'])
def mark_completed(transaction_id):
    # Check if user is logged in
    if 'username' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login_page'))
        
    if session.get('user_role') != 'B':
        flash('Only User B can mark services as completed', 'error')
        return redirect(url_for('index'))
    
    result = midpay.mark_service_completed(transaction_id)
    
    if result["status"] == "success":
        flash('Service marked as completed!', 'success')
    else:
        flash(f'Error: {result["message"]}', 'error')
    
    return redirect(url_for('index'))

@app.route('/confirm_transaction/<transaction_id>', methods=['POST'])
def confirm_transaction(transaction_id):
    # Check if user is logged in
    if 'username' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login_page'))
        
    if session.get('user_role') != 'A':
        flash('Only User A can confirm transactions', 'error')
        return redirect(url_for('index'))
    
    result = midpay.confirm_completion(transaction_id)
    
    if result["status"] == "success":
        flash('Transaction confirmed and payment released!', 'success')
    else:
        flash(f'Error: {result["message"]}', 'error')
    
    return redirect(url_for('index'))

@app.route('/cancel_transaction/<transaction_id>', methods=['POST'])
def cancel_transaction(transaction_id):
    # Check if user is logged in
    if 'username' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login_page'))
        
    if session.get('user_role') != 'A':
        flash('Only User A can cancel transactions', 'error')
        return redirect(url_for('index'))
    
    result = midpay.cancel_transaction(transaction_id)
    
    if result["status"] == "success":
        flash('Transaction cancelled and funds returned!', 'success')
    else:
        flash(f'Error: {result["message"]}', 'error')
    
    return redirect(url_for('index'))

@app.route('/transaction/<transaction_id>')
def view_transaction(transaction_id):
    # Check if user is logged in
    if 'username' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login_page'))
        
    result = midpay.get_transaction_status(transaction_id)
    
    if result["status"] == "success":
        transaction = result["transaction"]
        transaction["id"] = transaction_id  # Add the ID to the transaction data
        return render_template('transaction.html', 
                              transaction=transaction, 
                              user_role=session.get('user_role', ''),
                              username=session.get('username', ''),
                              name=session.get('name', ''))
    else:
        flash(f'Error: {result["message"]}', 'error')
        return redirect(url_for('index'))

@app.route('/verify_blockchain')
def verify_blockchain():
    # Check if user is logged in
    if 'username' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login_page'))
        
    result = midpay.verify_blockchain()
    
    if result["status"] == "success":
        flash('Blockchain verified successfully!', 'success')
    else:
        flash(f'Blockchain verification failed: {result["message"]}', 'error')
    
    return redirect(url_for('index'))

@app.route('/api-docs')
def api_docs():
    """Render the API documentation page"""
    return render_template('api_documentation.html',
                          username=session.get('username', ''),
                          name=session.get('name', ''),
                          user_role=session.get('user_role', ''))

@app.route('/get-api-key')
def get_api_key():
    """Generate and return an API key for the logged-in user"""
    # Check if user is logged in
    if 'username' not in session:
        flash('Please login to get an API key', 'error')
        return redirect(url_for('login_page'))
    
    # Get user information from the session
    name = session.get('name')
    email = session.get('email')
    
    # Generate API key using the imported function
    api_key = generate_api_key(name, email)
    
    # Save the generated API key
    save_api_key(email, api_key)
    
    # Return the key to the user
    return render_template('api_key.html',
                          api_key=api_key,
                          username=session.get('username', ''),
                          name=session.get('name', ''),
                          user_role=session.get('user_role', ''))

@app.route('/profile')
def profile():
    """Render user profile page with all user-related data"""
    # Check if user is logged in
    if 'username' not in session:
        flash('Please login to view your profile', 'info')
        return redirect(url_for('login_page'))
    
    # Load user data
    user_data = load_users()
    current_user = next((u for u in user_data['users'] if u['username'] == session['username']), None)
    
    if not current_user:
        flash('User data not found', 'error')
        return redirect(url_for('dashboard'))
    
    # Get user transactions
    user_transactions = []
    for tx_id in midpay.transactions:
        tx_info = midpay.get_transaction_status(tx_id)
        if tx_info["status"] == "success":
            tx_data = tx_info["transaction"]
            tx_data["id"] = tx_id  # Add transaction ID to the data
            user_transactions.append(tx_data)
    
    # Get user balance based on role
    user_role = session.get('user_role')
    balance = midpay.get_balance(user_role)
    
    # Get transaction statistics
    transaction_stats = {
        "total": len(user_transactions),
        "pending": sum(1 for tx in user_transactions if tx["status"] == "pending"),
        "completed": sum(1 for tx in user_transactions if tx["status"] == "completed"),
        "released": sum(1 for tx in user_transactions if tx["status"] == "released"),
        "cancelled": sum(1 for tx in user_transactions if tx["status"] == "cancelled"),
    }
    
    # Check if user has API key
    has_api_key = False
    try:
        with open('validkeys.json', 'r') as file:
            valid_keys = json.load(file)
            has_api_key = session.get('email', '') in valid_keys.values()
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    
    return render_template('profile.html', 
                           user=current_user,
                           balance=balance,
                           transactions=user_transactions,
                           transaction_stats=transaction_stats,
                           has_api_key=has_api_key,
                           username=session.get('username', ''),
                           name=session.get('name', ''),
                           user_role=session.get('user_role', ''))

if __name__ == '__main__':
    app.run(debug=True, port=8000)  # Using port 8000 to avoid conflict with the API