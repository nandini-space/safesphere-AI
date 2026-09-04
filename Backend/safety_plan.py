# ==========================================
# SAFESPHERE SAFETY PLAN GENERATOR
# ==========================================


def generate_safety_plan(level, indicators=None):
    """
    Generate calm and practical next steps
    based on the assessed risk level.
    """

    if indicators is None:
        indicators = []

    # Extract indicator names
    indicator_names = []

    for indicator in indicators:

        if isinstance(indicator, dict):
            name = indicator.get("name")

            if isinstance(name, str):
                indicator_names.append(name.lower())

        elif isinstance(indicator, str):
            indicator_names.append(indicator.lower())

    # Remove duplicates
    indicator_names = list(set(indicator_names))


    # ==========================================
    # LOW RISK
    # ==========================================

    if level == "LOW":

        return {
            "message": (
                "We found limited signs of immediate concern. "
                "It may still be useful to stay aware of how the interaction develops."
            ),

            "steps": [
                "Take your time before responding to unexpected requests.",
                "Avoid sharing sensitive information unless you are confident about the person or situation.",
                "Save important messages if the situation changes."
            ]
        }


    # ==========================================
    # MODERATE RISK
    # ==========================================

    elif level == "MODERATE":

        return {
            "message": (
                "Some patterns in this interaction may deserve extra attention. "
                "Consider slowing down and gathering more context before taking action."
            ),

            "steps": [
                "Do not feel pressured to respond immediately.",
                "Verify the person's identity or request through another trusted channel.",
                "Avoid sharing money, passwords, OTPs, or sensitive personal information.",
                "Keep relevant messages or screenshots if you may need them later."
            ]
        }


    # ==========================================
    # HIGH RISK
    # ==========================================

    elif level == "HIGH":

        return {
            "message": (
                "We found several concerning patterns. "
                "Consider pausing further interaction until you have more support or clarity."
            ),

            "steps": [
                "Avoid sending money or sensitive information.",
                "Do not respond under pressure or threats.",
                "Preserve relevant messages, screenshots, or other evidence.",
                "Consider discussing the situation with someone you trust.",
                "Use the platform's blocking or reporting tools if appropriate."
            ]
        }


    # ==========================================
    # CRITICAL RISK
    # ==========================================

    elif level == "CRITICAL":

        return {
            "message": (
                "This interaction contains multiple strong warning signs. "
                "Prioritize your immediate safety and avoid making rushed decisions."
            ),

            "steps": [
                "Stop sharing money, passwords, OTPs, or sensitive information.",
                "Do not respond to threats or pressure with rushed decisions.",
                "Preserve relevant messages, screenshots, and other evidence.",
                "Contact someone you trust and explain what is happening.",
                "Consider blocking and reporting the account or platform interaction.",
                "If you believe there is an immediate danger, contact appropriate local emergency services."
            ]
        }


    # ==========================================
    # DEFAULT
    # ==========================================

    return {
        "message": (
            "We could not determine a specific safety level. "
            "Please review the interaction carefully and avoid sharing sensitive information."
        ),

        "steps": [
            "Take your time before making decisions.",
            "Avoid responding to pressure.",
            "Seek support from someone you trust if you feel uncomfortable."
        ]
    }


# ==========================================
# TEST SAFETY PLAN
# ==========================================

if __name__ == "__main__":

    test_level = "HIGH"

    test_indicators = [
        {
            "name": "threat",
            "severity": 3
        },
        {
            "name": "secrecy",
            "severity": 2
        }
    ]

    result = generate_safety_plan(
        test_level,
        test_indicators
    )

    print(result)