import requests

# Define the URL to which you want to send the POST request
url = "https://secrets-api.appbrewery.com/get-auth-token"  # Replace with your API endpoint
deleteUrl = "https://secrets-api.appbrewery.com/secrets/"  # Replace with your API endpoint

# Data to be sent in the POST request (if needed)
data = {
    "username": "TRD7iZrd5gATjj9PkPEuaOlfEjHqj32V",
    "password": "TRD7iZrd5gATjj9PkPEuaOlfEjHqj32V",
}

# Proxy settings
proxy_url = "localhost:7770"  # Replace with the proxy IP and port
proxies = {
    "http": f"http://{proxy_url}",
    "https": f"https://{proxy_url}",
}

response = requests.post(url, data=data, proxies=proxies)

token = response.json()["token"]  # Access the 'token' key from the JSON response

print(token)

# Perform the DELETE request with the Bearer Token in the headers
headers = {
    "Authorization": f"Bearer {token}",  # Include the Bearer Token in the Authorization header
}

params = {"id": 52}  # Replace with the desired ID to delete
response = requests.delete(deleteUrl, params=params, headers=headers, proxies=proxies)

if response.status_code == 200:
    print("Resource deleted successfully.")
elif response.status_code == 404:
    print("Resource not found. The specified ID does not exist.")
else:
    print(f"Failed to delete resource with status code: {response.status_code}")
    print(response.json())  # Print the error response for debugging purposes
