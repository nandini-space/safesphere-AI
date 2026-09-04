# ==========================================
# SAFESPHERE ESCALATION TIMELINE
# ==========================================


# Define the order in which concerning behavior
# may escalate during an interaction
ESCALATION_STAGES = {
    "boundary_testing": {
        "stage": 1,
        "label": "Boundary Testing",
        "level": "LOW",
        "description": (
            "The interaction may include attempts to test "
            "what the person is comfortable sharing or doing."
        )
    },

    "manipulation": {
        "stage": 2,
        "label": "Manipulation",
        "level": "MODERATE",
        "description": (
            "The interaction may include attempts to influence "
            "feelings, guilt, fear, or responsibility."
        )
    },

    "secrecy": {
        "stage": 3,
        "label": "Secrecy",
        "level": "MODERATE",
        "description": (
            "The person may be encouraging the interaction "
            "to remain hidden from trusted people."
        )
    },

    "urgency": {
        "stage": 4,
        "label": "Urgency",
        "level": "MODERATE",
        "description": (
            "The interaction may include pressure to act "
            "quickly without enough time to think."
        )
    },

    "pressure": {
        "stage": 5,
        "label": "Pressure",
        "level": "HIGH",
        "description": (
            "The interaction may involve repeated or strong "
            "pressure to take an action."
        )
    },

    "financial_request": {
        "stage": 6,
        "label": "Financial Request",
        "level": "HIGH",
        "description": (
            "The interaction includes a request involving "
            "money or financial information."
        )
    },

    "sensitive_information_request": {
        "stage": 6,
        "label": "Sensitive Information Request",
        "level": "HIGH",
        "description": (
            "The interaction includes a request for private "
            "or sensitive information."
        )
    },

    "coercion": {
        "stage": 7,
        "label": "Coercion",
        "level": "HIGH",
        "description": (
            "The interaction may involve force, fear, "
            "or pressure that makes refusal difficult."
        )
    },

    "threat": {
        "stage": 8,
        "label": "Threat",
        "level": "CRITICAL",
        "description": (
            "The interaction includes threatening language "
            "or possible consequences intended to intimidate."
        )
    }
}


def generate_escalation_timeline(indicators):
    """
    Generate an ordered timeline based on
    indicators detected by the AI.
    """

    timeline = []

    if not isinstance(indicators, list):
        return timeline

    added_indicators = set()

    for indicator in indicators:

        # Get indicator name
        if isinstance(indicator, dict):
            indicator_name = indicator.get("name", "")

            evidence = indicator.get("evidence", "")

        elif isinstance(indicator, str):
            indicator_name = indicator
            evidence = ""

        else:
            continue

        # Validate name
        if not isinstance(indicator_name, str):
            continue

        indicator_name = indicator_name.lower().strip()

        # Avoid duplicates
        if indicator_name in added_indicators:
            continue

        # Check if indicator exists in timeline mapping
        if indicator_name in ESCALATION_STAGES:

            stage_data = ESCALATION_STAGES[indicator_name]

            timeline.append({
                "stage": stage_data["stage"],
                "indicator": indicator_name,
                "label": stage_data["label"],
                "level": stage_data["level"],
                "description": stage_data["description"],
                "evidence": evidence
            })

            added_indicators.add(indicator_name)

    # Sort by escalation stage
    timeline.sort(
        key=lambda item: item["stage"]
    )

    return timeline


# ==========================================
# TEST THE TIMELINE
# ==========================================

if __name__ == "__main__":

    test_indicators = [
        {
            "name": "secrecy",
            "severity": 2,
            "evidence": "Do not tell anyone about this."
        },
        {
            "name": "pressure",
            "severity": 3,
            "evidence": "You need to do this now."
        },
        {
            "name": "threat",
            "severity": 4,
            "evidence": "You will regret it if you refuse."
        }
    ]

    result = generate_escalation_timeline(
        test_indicators
    )

    print(result)