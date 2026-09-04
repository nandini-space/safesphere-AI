import requests

data = {
    "case_name": "Suspicious Online Contact",

    "summary": (
        "The conversation contains repeated pressure "
        "and requests for secrecy."
    ),

    "indicators": [
        {
            "name": "pressure",
            "severity": 3
        },
        {
            "name": "secrecy",
            "severity": 3
        }
    ],

    "context": {
        "unknown_sender": True
    },

    "answers": {}
}


response = requests.post(
    "http://127.0.0.1:5000/assess",
    json=data
)

print("Status Code:", response.status_code)
print("Response:")
print(response.json())