from flask import Flask, request, jsonify
from flask_cors import CORS
from risk_engine import calculate_risk

app = Flask(__name__)
CORS(app)


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json(silent=True)

    if data is None:
        return jsonify({
            "error": "No JSON data provided"
        }), 400

    text = data.get("text")

    if not text:
        return jsonify({
            "error": "Text is required"
        }), 400

    return jsonify({
        "success": True,
        "message": "Analysis endpoint is working",
        "received_text": text,
        "indicators": [],
        "questions": []
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