from flask import Flask, request, jsonify
from flask_cors import CORS

from risk_engine import calculate_risk
from safety_plan import generate_safety_plan
from escalation_timeline import generate_escalation_timeline
from AI.analyzer import analyze_conversation
from supabase_client import supabase


# ==========================================
# CREATE FLASK APPLICATION
# ==========================================

app = Flask(__name__)

# Allow frontend to communicate with backend
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

    except Exception as e:
        print("Analysis error:", str(e))

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

    # Check if AI analyzer returned an error
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
        print("Missing AI fields:", missing_fields)

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


    # ==========================================
    # GET CASE INFORMATION
    # ==========================================

    case_name = data.get(
        "case_name",
        "SafeSphere Analysis"
    )

    summary = data.get(
        "summary",
        ""
    )


    # ==========================================
    # GET ANALYSIS DATA
    # ==========================================

    indicators = data.get("indicators")

    context = data.get(
        "context",
        {}
    )

    answers = data.get(
        "answers",
        {}
    )


    # ==========================================
    # VALIDATE INPUT
    # ==========================================

    if not indicators:
        return jsonify({
            "success": False,
            "error": "Indicators are required"
        }), 400

    if not isinstance(indicators, list):
        return jsonify({
            "success": False,
            "error": "Indicators must be a list"
        }), 400

    if not isinstance(context, dict):
        return jsonify({
            "success": False,
            "error": "Context must be an object"
        }), 400

    if not isinstance(answers, dict):
        return jsonify({
            "success": False,
            "error": "Answers must be an object"
        }), 400


    # ==========================================
    # CALCULATE RISK
    # ==========================================

    try:

        assessment = calculate_risk(
            indicators,
            context,
            answers
        )

    except Exception as e:

        print("Risk engine error:", str(e))

        return jsonify({
            "success": False,
            "error": "Unable to calculate risk assessment"
        }), 500


    # ==========================================
    # GENERATE SAFETY PLAN
    # ==========================================

    try:

        safety_plan = generate_safety_plan(
            assessment["level"],
            indicators
        )

    except Exception as e:

        print("Safety plan error:", str(e))

        safety_plan = []


    # ==========================================
    # GENERATE ESCALATION TIMELINE
    # ==========================================

    try:

        timeline = generate_escalation_timeline(
            indicators
        )

    except Exception as e:

        print("Timeline error:", str(e))

        timeline = []


    # ==========================================
    # SAVE TO EVIDENCE VAULT
    # ==========================================

    saved_case = None
    vault_saved = False

    try:

        vault_data = {
            "case_name": case_name,
            "summary": summary,
            "concern_level": assessment.get("level"),
            "risk_score": assessment.get("score"),
            "indicators": indicators,
            "timeline": timeline,
            "safety_plan": safety_plan
        }

        response = (
            supabase
            .table("evidence_vault")
            .insert(vault_data)
            .execute()
        )

        if response.data:

            saved_case = response.data[0]

            vault_saved = True

            print(
                "Evidence saved successfully! "
                f"Case ID: {saved_case.get('id')}"
            )

    except Exception as e:

        print(
            "Evidence Vault save error:",
            str(e)
        )


    # ==========================================
    # RETURN FINAL RESULT
    # ==========================================

    return jsonify({

        "success": True,

        "assessment": assessment,

        "safety_plan": safety_plan,

        "escalation_timeline": timeline,

        "vault_saved": vault_saved,

        "saved_case": saved_case

    }), 200


# ==========================================
# HEALTH CHECK ENDPOINT
# ==========================================

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "success": True,
        "message": "SafeSphere Backend is running"
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