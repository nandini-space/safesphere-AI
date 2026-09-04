import requests
import json

url = "http://127.0.0.1:5000/analyze"

data = {
    "text": """
Person A: Kisi ko mat batana.
Person A: Jaldi karo and send it now.
Person A: You have to do this immediately.
"""
}

response = requests.post(
    url,
    json=data
)

print("Status Code:", response.status_code)
print("\nResponse:\n")

try:
    print(json.dumps(response.json(), indent=4))
except Exception:
    print(response.text)