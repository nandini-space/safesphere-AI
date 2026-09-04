from flask import Flask, request, jsonify
from flask_cors import CORS
from risk_engine import calculate_risk
from AI.analyzer import analyze_conversation

app = Flask(__name__)
CORS(app)

@app.route("/analyze", methods=["POST"])
def analyze():
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

    # Send conversation to Member 2's AI analyzer
    try:
        analysis = analyze_conversation(text)
    except Exception:
        return jsonify({
            "success": False,
            "error": "Analysis service is temporarily unavailable. Please try again."
        }), 503

    # Check whether the analyzer returned an error
    if not isinstance(analysis, dict):
        return jsonify({
            "success": False,
            "error": "Invalid response from analysis service"
        }), 502

    if analysis.get("error"):
        return jsonify({
            "success": False,
            "error": analysis["error"]
        }), 502

    # Validate the expected AI response structure
    required_fields = [
        "summary",
        "indicators",
        "concern_level",
        "needs_context",
        "questions"
    ]

    missing_fields = [
        field for field in required_fields
        if field not in analysis
    ]

    if missing_fields:
        return jsonify({
            "success": False,
            "error": "Invalid response from analysis service"
        }), 502

    # Return the validated analysis
    return jsonify({
        "success": True,
        "analysis": analysis
    }), 200

@app.route("/assess", methods=["POST"])
def assess():
    data = request.get_json(silent=True)

    # Check if JSON was provided
    if data is None:
        return jsonify({
            "success": False,
            "error": "No JSON data provided"
        }), 400

    # Get indicators and context
    indicators = data.get("indicators")
    context = data.get("context", {})

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

    # Context must be an object/dictionary
    if not isinstance(context, dict):
        return jsonify({
            "success": False,
            "error": "Context must be an object"
        }), 400

    # Calculate risk
    assessment = calculate_risk(indicators, context)

    # Return result
    return jsonify({
        "success": True,
        "assessment": assessment
    }), 200

if __name__ == "__main__":
    app.run(debug=True)