from flask import Flask, request, jsonify
from flask_cors import CORS

from risk_engine import calculate_risk
from safety_plan import generate_safety_plan
from AI.analyzer import analyze_conversation


# Create Flask application
app = Flask(__name__)

# Enable frontend to communicate with backend
CORS(app)


# ==========================================
# ANALYZE CONVERSATION ENDPOINT
# ==========================================

@app.route("/analyze", methods=["POST"])
def analyze():

    # Get JSON data safely
    data = request.get_json(silent=True)

    # Check if JSON was provided
    if data is None:
        return jsonify({
            "success": False,
            "error": "No JSON data provided"
        }), 400

    # Get conversation text
    text = data.get("text")

    # Validate text
    if not isinstance(text, str) or not text.strip():
        return jsonify({
            "success": False,
            "error": "Text is required"
        }), 400

    # Send conversation to AI analyzer
    try:
        analysis = analyze_conversation(text)

    except Exception:
        return jsonify({
            "success": False,
            "error": "Analysis service is temporarily unavailable. Please try again."
        }), 503

    # Validate analyzer response
    if not isinstance(analysis, dict):
        return jsonify({
            "success": False,
            "error": "Invalid response from analysis service"
        }), 502

    # Check if AI returned an error
    if analysis.get("error"):
        return jsonify({
            "success": False,
            "error": analysis["error"]
        }), 502

    # Expected fields from AI analyzer
    required_fields = [
        "summary",
        "indicators",
        "concern_level",
        "needs_context",
        "questions"
    ]

    # Check for missing fields
    missing_fields = [
        field
        for field in required_fields
        if field not in analysis
    ]

    if missing_fields:
        return jsonify({
            "success": False,
            "error": "Invalid response from analysis service"
        }), 502

    # Return AI analysis
    return jsonify({
        "success": True,
        "analysis": analysis
    }), 200


# ==========================================
# FINAL RISK ASSESSMENT ENDPOINT
# ==========================================

@app.route("/assess", methods=["POST"])
def assess():

    # Get JSON data safely
    data = request.get_json(silent=True)

    # Check if JSON was provided
    if data is None:
        return jsonify({
            "success": False,
            "error": "No JSON data provided"
        }), 400

    # Get indicators
    indicators = data.get("indicators")

    # Get optional user context
    context = data.get("context", {})

    # Get optional answers
    answers = data.get("answers", {})

    # Validate indicators
    if not indicators:
        return jsonify({
            "success": False,
            "error": "Indicators are required"
        }), 400

    # Indicators must be a list
    if not isinstance(indicators, list):
        return jsonify({
            "success": False,
            "error": "Indicators must be a list"
        }), 400

    # Context must be a dictionary
    if not isinstance(context, dict):
        return jsonify({
            "success": False,
            "error": "Context must be an object"
        }), 400

    # Answers must be a dictionary
    if not isinstance(answers, dict):
        return jsonify({
            "success": False,
            "error": "Answers must be an object"
        }), 400

    # ==========================================
    # CALCULATE RISK
    # ==========================================

    assessment = calculate_risk(
        indicators,
        context,
        answers
    )

    # ==========================================
    # GENERATE SAFETY PLAN
    # ==========================================

    safety_plan = generate_safety_plan(
        assessment["level"],
        indicators
    )

    # ==========================================
    # RETURN FINAL RESULT
    # ==========================================

    return jsonify({
        "success": True,
        "assessment": assessment,
        "safety_plan": safety_plan
    }), 200


# ==========================================
# RUN FLASK SERVER
# ==========================================

if __name__ == "__main__":
    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )