from dotenv import load_dotenv
from openai import OpenAI
import os
import json


# Load environment variables from .env
load_dotenv()


# Get Featherless API key
API_KEY = os.getenv("FEATHERLESS_API_KEY")


# Connect to Featherless AI
client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.featherless.ai/v1"
)


# Controlled list of allowed indicators
ALLOWED_INDICATORS = [
    "urgency",
    "secrecy",
    "pressure",
    "manipulation",
    "boundary_testing",
    "coercion",
    "threat",
    "financial_request",
    "sensitive_information_request",
    "repeated_contact"
]


# Allowed concern levels
ALLOWED_CONCERN_LEVELS = [
    "LOW",
    "MODERATE",
    "HIGH",
    "CRITICAL"
]


# Fixed question templates based on detected indicators
QUESTION_TEMPLATES = {
    "urgency": [
        "Were you pressured to respond or act immediately?"
    ],
    "secrecy": [
        "Were you asked to hide this interaction from someone you trust?"
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

    for indicator in indicators:
        name = indicator.get("name")

        if name in QUESTION_TEMPLATES:
            for question_text in QUESTION_TEMPLATES[name]:
                questions.append({
                    "id": f"q{question_number}",
                    "question": question_text,
                    "type": "multiple_choice"
                })

                question_number += 1

    return questions


def calculate_concern_level(indicators):
    """Calculate concern level based on the highest indicator severity."""

    if not indicators:
        return "LOW"

    highest_severity = max(
        indicator["severity"] for indicator in indicators
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
    """Validate the AI response and return a consistent SafeSphere format."""

    if not isinstance(data, dict):
        return {
            "error": "AI response is not a valid JSON object"
        }

    # Validate summary
    summary = data.get("summary", "")

    if not isinstance(summary, str):
        summary = ""

    # Validate indicators
    indicators = data.get("indicators", [])

    if not isinstance(indicators, list):
        indicators = []

    valid_indicators = []

    for indicator in indicators:

        if not isinstance(indicator, dict):
            continue

        name = indicator.get("name")

        # Keep only allowed indicators
        if name in ALLOWED_INDICATORS:

            severity = indicator.get("severity", 1)

            # Ensure severity is an integer
            if not isinstance(severity, int):
                severity = 1

            # Keep severity between 1 and 4
            severity = max(1, min(severity, 4))

            evidence = indicator.get("evidence", "")

            if not isinstance(evidence, str):
                evidence = ""

            valid_indicators.append({
                "name": name,
                "severity": severity,
                "evidence": evidence
            })

    # Calculate concern level from validated indicator severities
    concern_level = calculate_concern_level(valid_indicators)

    # Validate needs_context
    needs_context = data.get("needs_context", False)

    if not isinstance(needs_context, bool):
        needs_context = False

    # Generate controlled questions based on indicators
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

3. Understand English, Hindi, Hinglish, and mixed languages.

4. Evaluate EACH allowed indicator independently.

5. A conversation may contain multiple indicators at the same time.
Do not return only the strongest indicator.
Return every indicator that is reasonably supported by the conversation.

6. Consider the meaning and context, not just exact English keywords.

Examples of meaning:
- "Kisi ko mat batana" or "Don't tell anyone" may indicate secrecy.
- "Jaldi karo", "Do it now", or "Send it immediately" may indicate urgency.
- Statements that make someone feel forced may indicate coercion or pressure.
- Threatening consequences may indicate threat.

7. Return ONLY valid JSON.
Do not use markdown or code fences.

8. Keep the summary concise and neutral.

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
    "concern_level": "LOW",
    "needs_context": false
}}

Severity rules:
1 = low
2 = moderate
3 = high
4 = critical

Concern levels allowed:
LOW
MODERATE
HIGH
CRITICAL

Conversation to analyze:

Before producing the final JSON, carefully check the entire conversation
against EVERY allowed indicator.

If more than one indicator is present, include all relevant indicators.

Conversation to analyze:

{conversation}
"""

    # Call Featherless AI
    try:
        response = client.chat.completions.create(
            model="Qwen/Qwen2.5-7B-Instruct",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

    except Exception as error:
        return {
            "error": "Featherless API request failed",
            "details": str(error)
        }

    # Get AI response
    result = response.choices[0].message.content.strip()

    # Remove markdown code fences if AI adds them
    if result.startswith("```json"):
        result = result.replace("```json", "", 1)

    elif result.startswith("```"):
        result = result.replace("```", "", 1)

    if result.endswith("```"):
        result = result.rsplit("```", 1)[0]

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
    print(json.dumps(result, indent=4, ensure_ascii=False))