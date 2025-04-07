import hashlib
import json
import os
import time

def generate_api_key(name, email):
    """Generate a unique API key using SHA-256."""
    # Create a unique string by combining name, email, and current timestamp
    unique_string = f"{name}_{email}_{time.time()}"
    # Generate SHA-256 hash
    hash_object = hashlib.sha256(unique_string.encode())
    # Return hexadecimal representation of the hash
    return hash_object.hexdigest()

def save_api_key(email, api_key):
    """Save the API key and email to validkeys.json."""
    json_file_path = "validkeys.json"
    data = {}
    
    # Check if the file exists and has content
    if os.path.exists(json_file_path) and os.path.getsize(json_file_path) > 0:
        with open(json_file_path, 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                # If the file exists but has invalid JSON content
                data = {}
    
    # Add the new key-email pair
    data[api_key] = email
    
    # Write the updated data back to the file
    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=4)

def main():
    print("API Key Generator")
    print("-----------------")
    
    # Get user input
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    
    # Validate email (basic validation)
    if '@' not in email or '.' not in email:
        print("Invalid email format. Please try again.")
        return
    
    # Generate API key
    api_key = generate_api_key(name, email)
    
    # Save the key
    save_api_key(email, api_key)
    
    print("\nAPI Key generated successfully!")
    print(f"Your API Key: {api_key}")
    print("This key has been stored in validkeys.json")

if __name__ == "__main__":
    main()
