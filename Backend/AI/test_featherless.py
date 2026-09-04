from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("FEATHERLESS_API_KEY"),
    base_url="https://api.featherless.ai/v1"
)

print("API key loaded:", bool(os.getenv("FEATHERLESS_API_KEY")))

response = client.chat.completions.create(
    model="Qwen/Qwen2.5-7B-Instruct",
    messages=[
        {
            "role": "user",
            "content": "Say hello to SafeSphere in one sentence."
        }
    ]
)

print(response.choices[0].message.content)