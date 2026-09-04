# ==========================================
# SAFESPHERE RISK ENGINE
# ==========================================


# Risk points for AI-detected indicators
INDICATOR_POINTS = {
    "secrecy": 15,
    "repeated_pressure": 15,
    "pressure": 15,
    "manipulation": 15,
    "boundary_testing": 10,
    "coercion": 25,
    "threat": 30,
    "financial_request": 20,
    "sensitive_information_request": 20,
    "repeated_contact": 10
}


# Risk points for user-provided context
CONTEXT_POINTS = {
    "unknown_sender": 10,
    "unexpected_interaction": 10,
    "repeated_behavior": 15
}


# Additional risk points based on user answers
ANSWER_POINTS = {
    "yes": 5,
    "maybe": 2,
    "no": 0
}


# ==========================================
# DETERMINE RISK LEVEL
# ==========================================

def get_risk_level(score):

    if score >= 70:
        return "CRITICAL"

    elif score >= 40:
        return "HIGH"

    elif score >= 20:
        return "MODERATE"

    else:
        return "LOW"


# ==========================================
# CALCULATE RISK
# ==========================================

def calculate_risk(indicators, context=None, answers=None):

    score = 0
    breakdown = []

    # Store indicators actually detected by AI
    detected_indicators = set()

    # --------------------------------------
    # 1. SCORE AI-DETECTED INDICATORS
    # --------------------------------------

    for indicator in indicators:

        # Format 1: simple string
        # Example: "secrecy"
        if isinstance(indicator, str):
            indicator_name = indicator.lower().strip()

        # Format 2: AI indicator object
        # Example:
        # {"name": "secrecy", "severity": 2}
        elif isinstance(indicator, dict):

            indicator_name = indicator.get("name", "")

            if not isinstance(indicator_name, str):
                continue

            indicator_name = indicator_name.lower().strip()

        # Ignore invalid formats
        else:
            continue

        # Only process known indicators
        if indicator_name in INDICATOR_POINTS:

            # Remember that AI detected this indicator
            detected_indicators.add(indicator_name)

            points = INDICATOR_POINTS[indicator_name]

            score += points

            breakdown.append({
                "type": "indicator",
                "indicator": indicator_name,
                "points": points
            })


    # --------------------------------------
    # 2. SCORE USER ANSWERS
    # --------------------------------------

    if answers:

        for indicator_name, answer in answers.items():

            # Indicator name must be text
            if not isinstance(indicator_name, str):
                continue

            indicator_name = indicator_name.lower().strip()

            # Only score answers for indicators
            # actually detected by the AI
            if indicator_name not in detected_indicators:
                continue

            # Answer must be text
            if not isinstance(answer, str):
                continue

            answer_value = answer.lower().strip()

            points = ANSWER_POINTS.get(answer_value, 0)

            if points > 0:

                score += points

                breakdown.append({
                    "type": "answer",
                    "indicator": indicator_name,
                    "answer": answer_value,
                    "points": points
                })


    # --------------------------------------
    # 3. SCORE USER CONTEXT
    # --------------------------------------

    if context:

        for context_name, enabled in context.items():

            if enabled and context_name in CONTEXT_POINTS:

                points = CONTEXT_POINTS[context_name]

                score += points

                breakdown.append({
                    "type": "context",
                    "indicator": context_name,
                    "points": points
                })


    # --------------------------------------
    # 4. LIMIT SCORE
    # --------------------------------------

    score = min(score, 100)


    # --------------------------------------
    # 5. DETERMINE FINAL LEVEL
    # --------------------------------------

    level = get_risk_level(score)


    # --------------------------------------
    # 6. RETURN RESULT
    # --------------------------------------

    return {
        "score": score,
        "level": level,
        "breakdown": breakdown
    }


# ==========================================
# TEST RISK ENGINE
# ==========================================

if __name__ == "__main__":

    # Indicators detected by AI
    test_indicators = [
        {
            "name": "secrecy",
            "severity": 2,
            "evidence": "Do not tell anyone."
        },
        {
            "name": "threat",
            "severity": 3,
            "evidence": "You will regret it."
        }
    ]


    # User context
    test_context = {
        "unknown_sender": True,
        "unexpected_interaction": True,
        "repeated_behavior": False
    }


    # User answers
    test_answers = {
        "coercion": "yes",   # Ignored: AI did not detect coercion
        "secrecy": "maybe",  # +2
        "threat": "yes"      # +5
    }


    # Calculate risk
    result = calculate_risk(
        test_indicators,
        test_context,
        test_answers
    )


    print(result)