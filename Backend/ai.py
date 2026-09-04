import os
import json
from openai import OpenAI
from dotenv import load_dotenv


# Load variables from .env file
load_dotenv()


# Get Featherless API details
FEATHERLESS_API_KEY = os.getenv("FEATHERLESS_API_KEY")
FEATHERLESS_MODEL = os.getenv("FEATHERLESS_MODEL")


# Check if API key exists
if not FEATHERLESS_API_KEY:
    raise ValueError(
        "FEATHERLESS_API_KEY is missing. Add it to your .env file."
    )


# Create Featherless AI client
client = OpenAI(
    base_url="https://api.featherless.ai/v1",
    api_key=FEATHERLESS_API_KEY
)


def analyze_conversation(text):
    """
    Analyze a conversation and return structured SafeSphere data.
    """

    if not isinstance(text, str) or not text.strip():
        raise ValueError("Text must be a non-empty string.")

    system_prompt = """
You are SafeSphere AI, a safety-focused conversation analysis assistant.

Your task is to analyze a conversation for possible concerning interaction patterns.

Look for ONLY these indicators when supported by the text:

- secrecy
- repeated_pressure
- pressure
- manipulation
- boundary_testing
- coercion
- threat
- financial_request
- sensitive_information_request
- repeated_contact

IMPORTANT RULES:

1. Do not diagnose people.
2. Do not claim certainty about someone's intentions.
3. Only identify indicators supported by the conversation.
4. Keep the language calm and non-alarmist.
5. Return ONLY valid JSON.
6. Do not include markdown.
7. Do not add explanations outside the JSON.

Return data in exactly this format:

{
  "summary": "short summary of the interaction",
  "indicators": [
    {
      "name": "indicator_name",
      "severity": 1,
      "evidence": "exact or closely relevant evidence from the text"
    }
  ],
  "concern_level": "LOW",
  "needs_context": false,
  "questions": [
    {
      "id": "q1",
      "question": "relevant question for the user",
      "type": "multiple_choice",
      "indicator": "related_indicator"
    }
  ]
}

Severity must be:
1 = mild
2 = moderate
3 = strong

Concern level must be one of:
LOW
MODERATE
HIGH
CRITICAL

Generate 0 to 3 relevant questions.

If there are no concerning indicators, return an empty indicators list.
"""

    try:
        response = client.chat.completions.create(
            model=FEATHERLESS_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": f"""
Analyze the following conversation:

{text}
"""
                }
            ],
            temperature=0.2,
            max_tokens=1000
        )

        ai_response = response.choices[0].message.content

        if not ai_response:
            raise ValueError("AI returned an empty response.")

        # Remove accidental markdown code blocks
        ai_response = ai_response.strip()

        if ai_response.startswith("```json"):
            ai_response = ai_response[7:]

        elif ai_response.startswith("```"):
            ai_response = ai_response[3:]

        if ai_response.endswith("```"):
            ai_response = ai_response[:-3]

        ai_response = ai_response.strip()

        # Convert AI response into Python dictionary
        result = json.loads(ai_response)

        return result

    except json.JSONDecodeError:
        raise ValueError(
            "AI returned an invalid JSON response."
        )

    except Exception as error:
        raise RuntimeError(
            f"AI analysis failed: {str(error)}"
        )