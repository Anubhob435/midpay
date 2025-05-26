import requests
#small commit
url = "http://localhost:5000/api/accounts"
headers = {
    "X-API-Key": "avhgavhgvd"
}

response = requests.get(url, headers=headers)
print(response.json())
