import os
import json

from dotenv import load_dotenv
from openai import OpenAI


# Load environment variables from .env
load_dotenv()


# Get Featherless API details
API_KEY = os.getenv("FEATHERLESS_API_KEY")
FEATHERLESS_MODEL = os.getenv("FEATHERLESS_MODEL")


# Create the provider client lazily so the Flask app can still start and return
# a helpful error when environment variables have not been configured yet.
client = None


def get_client():
    global client
    if client is None:
        client = OpenAI(
            api_key=API_KEY,
            base_url="https://api.featherless.ai/v1",
            timeout=60.0,
            max_retries=0,
        )
    return client


# Controlled list of allowed indicators
ALLOWED_INDICATORS = [
    "urgency",
    "secrecy",
    "repeated_pressure",
    "pressure",
    "manipulation",
    "boundary_testing",
    "coercion",
    "threat",
    "financial_request",
    "sensitive_information_request",
    "repeated_contact"
]


# Fixed question templates based on detected indicators
QUESTION_TEMPLATES = {
    "urgency": [
        "Were you pressured to respond or act immediately?"
    ],
    "secrecy": [
        "Were you asked to hide this interaction from someone you trust?"
    ],
    "repeated_pressure": [
        "Has the person continued pressuring you after you hesitated or refused?"
    ],
    "pressure": [
        "Did you feel pressured to do something you did not want to do?"
    ],
    "manipulation": [
        "Did the person try to make you feel guilty, afraid, or responsible?"
    ],
    "boundary_testing": [
        "Has this person gradually asked you to do things that made you uncomfortable?"
    ],
    "coercion": [
        "Did you feel forced or afraid to comply with the request?"
    ],
    "threat": [
        "Has this person made similar threats before?"
    ],
    "financial_request": [
        "Were you asked to send money, payment details, or financial information?"
    ],
    "sensitive_information_request": [
        "Were you asked to share private information such as passwords, OTPs, or personal details?"
    ],
    "repeated_contact": [
        "Has this person continued contacting you after you tried to stop or ignore them?"
    ]
}


def generate_dynamic_questions(indicators):
    """Generate relevant follow-up questions based on detected indicators."""

    questions = []
    question_number = 1

    # Limit to 3 questions for a cleaner MVP experience
    for indicator in indicators:
        name = indicator.get("name")

        if name in QUESTION_TEMPLATES:
            for question_text in QUESTION_TEMPLATES[name]:

                if len(questions) >= 3:
                    return questions

                questions.append({
                    "id": f"q{question_number}",
                    "question": question_text,
                    "type": "multiple_choice",
                    "indicator": name
                })

                question_number += 1

    return questions


def calculate_concern_level(indicators):
    """
    Calculate a preliminary AI concern level.

    The final risk level should come from risk_engine.py
    after user context and answers are included.
    """

    if not indicators:
        return "LOW"

    highest_severity = max(
        indicator.get("severity", 1)
        for indicator in indicators
    )

    if highest_severity == 1:
        return "LOW"

    elif highest_severity == 2:
        return "MODERATE"

    elif highest_severity == 3:
        return "HIGH"

    else:
        return "CRITICAL"


def validate_analysis(data):
    """Validate AI response and return a consistent SafeSphere format."""

    if not isinstance(data, dict):
        return {
            "error": "AI response is not a valid JSON object"
        }

    # Validate summary
    summary = data.get("summary", "")

    if not isinstance(summary, str):
        summary = ""

    summary = summary.strip()

    # Validate indicators
    indicators = data.get("indicators", [])

    if not isinstance(indicators, list):
        indicators = []

    valid_indicators = []
    seen_indicators = set()

    for indicator in indicators:

        if not isinstance(indicator, dict):
            continue

        name = indicator.get("name", "")

        if not isinstance(name, str):
            continue

        name = name.lower().strip()

        # Keep only allowed indicators
        if name not in ALLOWED_INDICATORS:
            continue

        # Avoid duplicate indicators
        if name in seen_indicators:
            continue

        severity = indicator.get("severity", 1)

        # Ensure severity is an integer
        if not isinstance(severity, int):
            severity = 1

        # Keep severity between 1 and 3
        severity = max(1, min(severity, 3))

        evidence = indicator.get("evidence", "")

        if not isinstance(evidence, str):
            evidence = ""

        evidence = evidence.strip()

        valid_indicators.append({
            "name": name,
            "severity": severity,
            "evidence": evidence
        })

        seen_indicators.add(name)

    # Calculate preliminary concern level
    concern_level = calculate_concern_level(valid_indicators)

    # Validate needs_context
    needs_context = data.get("needs_context", False)

    if not isinstance(needs_context, bool):
        needs_context = False

    # Generate controlled questions
    questions = generate_dynamic_questions(valid_indicators)

    # Return one fixed response contract
    return {
        "summary": summary,
        "indicators": valid_indicators,
        "concern_level": concern_level,
        "needs_context": needs_context,
        "questions": questions
    }


def analyze_conversation(conversation):
    """Send a conversation to Featherless AI and return structured analysis."""

    # Check API key
    if not API_KEY:
        return {
            "error": "FEATHERLESS_API_KEY is missing"
        }

    # Check model
    if not FEATHERLESS_MODEL:
        return {
            "error": "FEATHERLESS_MODEL is missing"
        }

    # Check empty conversation
    if not isinstance(conversation, str) or not conversation.strip():
        return {
            "error": "Conversation cannot be empty"
        }

    prompt = f"""
You are the AI analysis engine for SafeSphere.

Analyze the meaning of the conversation for potential safety concerns.

IMPORTANT RULES:

1. Only use indicators from this allowed list:

{ALLOWED_INDICATORS}

2. Do not invent new indicator names.

3. Only identify indicators supported by the conversation.

4. Understand English, Hindi, Hinglish, and mixed languages.

5. Evaluate EACH allowed indicator independently.

6. A conversation may contain multiple indicators at the same time.
Do not return only the strongest indicator.
Return every indicator that is reasonably supported by the conversation.

7. Consider the meaning and context, not just exact English keywords.

Examples of meaning:
- "Kisi ko mat batana" or "Don't tell anyone" may indicate secrecy.
- "Jaldi karo", "Do it now", or "Send it immediately" may indicate urgency.
- Statements that make someone feel forced may indicate coercion or pressure.
- Threatening consequences may indicate threat.

8. Do not diagnose people or claim certainty about someone's intentions.

9. Return ONLY valid JSON.
Do not use markdown or code fences.

10. Keep the summary concise, neutral, and calm.

Use exactly this structure:

{{
    "summary": "short summary of the conversation",
    "indicators": [
        {{
            "name": "indicator_name",
            "severity": 1,
            "evidence": "exact relevant text from conversation"
        }}
    ],
    "needs_context": false
}}

Severity rules:

1 = mild
2 = moderate
3 = strong

If there are no concerning indicators:

- return an empty indicators list
- set needs_context to false

Conversation to analyze:

Before producing the final JSON, carefully check the entire conversation
against EVERY allowed indicator.

If more than one indicator is present, include all relevant indicators.

Conversation to analyze:

{conversation}
"""

    # Call Featherless AI
    try:
        response = get_client().chat.completions.create(
            model=FEATHERLESS_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            max_tokens=1000
        )

    except Exception as error:
        return {
            "error": "Featherless API request failed",
            "details": str(error)
        }

    # Validate response
    if not response.choices:
        return {
            "error": "Featherless returned no choices"
        }

    # Get AI response
    result = response.choices[0].message.content

    if not result:
        return {
            "error": "Featherless returned an empty response"
        }

    result = result.strip()

    # Remove markdown code fences if AI adds them
    if result.startswith("```json"):
        result = result[7:]

    elif result.startswith("```"):
        result = result[3:]

    if result.endswith("```"):
        result = result[:-3]

    result = result.strip()

    # Convert AI JSON string to Python dictionary
    try:
        data = json.loads(result)

        return validate_analysis(data)

    except json.JSONDecodeError:
        return {
            "error": "AI returned invalid JSON",
            "raw_response": result
        }


# Test the AI engine directly
# Test the AI engine directly
# Test the AI engine directly
if __name__ == "__main__":

    test_conversation = """
Person A: Kisi ko mat batana. Jaldi karo and send it now.
"""

    result = analyze_conversation(test_conversation)

    print("\nAI ANALYSIS:\n")

    print(
        json.dumps(
            result,
            indent=4,
            ensure_ascii=False
        )
    )
