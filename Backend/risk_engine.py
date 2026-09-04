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


def get_risk_level(score):
    if score >= 70:
        return "CRITICAL"
    elif score >= 40:
        return "HIGH"
    elif score >= 20:
        return "MODERATE"
    else:
        return "LOW"


def calculate_risk(indicators, context=None):
    score = 0
    breakdown = []

    # Calculate points from indicators
    for indicator in indicators:
        indicator_name = indicator.lower().strip()
        points = INDICATOR_POINTS.get(indicator_name, 0)

        if points > 0:
            score += points

            breakdown.append({
                "type": "indicator",
                "indicator": indicator_name,
                "points": points
            })

    # Calculate points from user context
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

    # Prevent score from exceeding 100
    score = min(score, 100)

    # Determine risk level
    level = get_risk_level(score)

    return {
        "score": score,
        "level": level,
        "breakdown": breakdown
    }

if __name__ == "__main__":

    test_indicators = [
        "secrecy",
        "pressure",
        "threat"
    ]

    test_context = {
        "unknown_sender": True,
        "unexpected_interaction": True,
        "repeated_behavior": False
    }

    result = calculate_risk(
        test_indicators,
        test_context
    )

    print(result)