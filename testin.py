import requests

url = "http://192.168.0.121:5000/api/accounts"
headers = {
    "X-API-Key": "2adce4844b0133b3047657e76c4bda9d0143c9752e8c6bf5599dd3fd80319167"
}

response = requests.get(url, headers=headers)
print(response.json())