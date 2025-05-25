# MidPay API Examples - Get Accounts with API Key

This document provides examples of how to call the MidPay API with an API key to get account information.

## Prerequisites

1. **Generate an API Key**: Run the following command to generate your API key:
   ```bash
   python generate_api_key.py
   ```

2. **Start the API Server**: Make sure the FastAPI server is running:
   ```bash
   python fast_api.py
   ```
   The API will be available at `http://localhost:8000`

## API Endpoints for Accounts

### Get All Accounts
- **Endpoint**: `GET /api/accounts`
- **Description**: Get balances for all accounts including escrow
- **Authentication**: Required (X-API-Key header)

### Get Individual User Balance
- **Endpoint**: `GET /api/balance/{user}`
- **Description**: Get balance for a specific user (A or B)
- **Authentication**: Required (X-API-Key header)

## Examples

### 1. Using cURL

```bash
# Get all accounts
curl -X GET "http://localhost:8000/api/accounts" \
  -H "X-API-Key: your_api_key_here" \
  -H "Content-Type: application/json"

# Get balance for user A
curl -X GET "http://localhost:8000/api/balance/A" \
  -H "X-API-Key: your_api_key_here" \
  -H "Content-Type: application/json"

# Get balance for user B
curl -X GET "http://localhost:8000/api/balance/B" \
  -H "X-API-Key: your_api_key_here" \
  -H "Content-Type: application/json"
```

### 2. Using Python (requests library)

```python
import requests

API_KEY = "your_api_key_here"
BASE_URL = "http://localhost:8000/api"

headers = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}

# Get all accounts
response = requests.get(f"{BASE_URL}/accounts", headers=headers)
if response.status_code == 200:
    data = response.json()
    print("All accounts:", data)
else:
    print("Error:", response.status_code, response.text)

# Get user A balance
response = requests.get(f"{BASE_URL}/balance/A", headers=headers)
if response.status_code == 200:
    data = response.json()
    print("User A balance:", data)
```

### 3. Using JavaScript (fetch API)

```javascript
const API_KEY = "your_api_key_here";
const BASE_URL = "http://localhost:8000/api";

const headers = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
};

// Get all accounts
async function getAllAccounts() {
    try {
        const response = await fetch(`${BASE_URL}/accounts`, {
            method: 'GET',
            headers: headers
        });
        
        if (response.ok) {
            const data = await response.json();
            console.log("All accounts:", data);
            return data;
        } else {
            console.error("Error:", response.status, await response.text());
        }
    } catch (error) {
        console.error("Request failed:", error);
    }
}

// Get user balance
async function getUserBalance(userId) {
    try {
        const response = await fetch(`${BASE_URL}/balance/${userId}`, {
            method: 'GET',
            headers: headers
        });
        
        if (response.ok) {
            const data = await response.json();
            console.log(`User ${userId} balance:`, data);
            return data;
        } else {
            console.error("Error:", response.status, await response.text());
        }
    } catch (error) {
        console.error("Request failed:", error);
    }
}

// Usage
getAllAccounts();
getUserBalance("A");
getUserBalance("B");
```

### 4. Using PowerShell

```powershell
$apiKey = "your_api_key_here"
$baseUrl = "http://localhost:8000/api"

$headers = @{
    "X-API-Key" = $apiKey
    "Content-Type" = "application/json"
}

# Get all accounts
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/accounts" -Method Get -Headers $headers
    Write-Host "All accounts:" -ForegroundColor Green
    $response | ConvertTo-Json -Depth 3
} catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Get user A balance
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/balance/A" -Method Get -Headers $headers
    Write-Host "User A balance:" -ForegroundColor Green
    $response | ConvertTo-Json
} catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}
```

## Expected Response Formats

### Get All Accounts Response
```json
{
  "status": "success",
  "accounts": {
    "A": 1000.0,
    "B": 500.0,
    "escrow": 250.0
  }
}
```

### Get User Balance Response
```json
{
  "status": "success",
  "balance": 1000.0
}
```

## Error Responses

### 401 Unauthorized (Invalid API Key)
```json
{
  "detail": "Invalid or missing API key"
}
```

### 400 Bad Request (Invalid User ID)
```json
{
  "detail": "Invalid user ID"
}
```

## Quick Start

1. **Generate API Key**:
   ```bash
   python generate_api_key.py
   ```

2. **Start API Server**:
   ```bash
   python fast_api.py
   ```

3. **Test API** (replace `YOUR_API_KEY` with actual key):
   ```bash
   curl -X GET "http://localhost:8000/api/accounts" \
     -H "X-API-Key: YOUR_API_KEY"
   ```

4. **Use Python Example**:
   ```bash
   # Edit api_example.py and set your API key
   python api_example.py
   ```

## Notes

- Replace `your_api_key_here` with your actual API key
- The API server runs on `http://localhost:8000` by default
- All requests require the `X-API-Key` header for authentication
- User IDs are case-sensitive ("A" and "B")
- API responses are in JSON format
