from supabase_client import supabase

data = {
    "case_name": "Test SafeSphere Case",
    "summary": "This is a test analysis saved from the backend.",
    "concern_level": "Moderate",
    "risk_score": 55,
    "indicators": [
        {
            "name": "pressure",
            "severity": 3
        }
    ],
    "timeline": [
        {
            "stage": "Initial Contact",
            "description": "The conversation started normally."
        }
    ],
    "safety_plan": [
        "Do not share personal information",
        "Talk to someone you trust"
    ]
}

response = supabase.table("evidence_vault").insert(data).execute()

print("Data inserted successfully!")
print(response.data)