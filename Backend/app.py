import os
import tempfile
from pathlib import Path

from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

from risk_engine import calculate_risk
from safety_plan import generate_safety_plan
from escalation_timeline import generate_escalation_timeline
from AI.analyzer import analyze_conversation
from supabase_client import supabase
from evidence_vault import get_cases, get_case


# ==========================================
# CREATE FLASK APPLICATION
# ==========================================

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

# Allow the local Vite development server to communicate with the API.
CORS(app, resources={r"/*": {"origins": [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]}})


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
        print("Analysis service error:", analysis["error"])
        return jsonify({
            "success": False,
            "error": "Analysis service is temporarily unavailable. Please try again."
        }), 503

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


def analyze_uploaded_file(analyzer, input_type):
    """Store a short-lived upload, extract text, and reuse the normal analyzer."""
    uploaded_file = request.files.get("file")
    if not uploaded_file or not uploaded_file.filename:
        return jsonify({"success": False, "error": "Please choose a file to analyze."}), 400

    filename = secure_filename(uploaded_file.filename)
    suffix = Path(filename).suffix.lower()
    allowed_extensions = {
        "image": {".png", ".jpg", ".jpeg", ".webp"},
        "audio": {".wav", ".mp3", ".m4a", ".webm"},
    }
    if suffix not in allowed_extensions[input_type]:
        return jsonify({"success": False, "error": "That file format is not supported."}), 400

    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temporary_file:
            temporary_path = temporary_file.name
            uploaded_file.save(temporary_path)

        result = analyzer(temporary_path)
        analysis = result.get("analysis") if isinstance(result, dict) else None
        if not isinstance(analysis, dict) or analysis.get("error"):
            error = result.get("error") or (analysis or {}).get("error") or "Unable to analyze this upload."
            return jsonify({"success": False, "error": error}), 503

        return jsonify({
            "success": True,
            "analysis": analysis,
            "extracted_text": result.get("extracted_text", "")
        }), 200
    except Exception as error:
        print(f"{input_type.title()} analysis error:", str(error))
        return jsonify({"success": False, "error": f"Unable to analyze this {input_type} right now. Please try again."}), 503
    finally:
        if temporary_path and os.path.exists(temporary_path):
            os.remove(temporary_path)


@app.route("/analyze/image", methods=["POST"])
def analyze_image_upload():
    from multimodal.image import analyze_image
    return analyze_uploaded_file(analyze_image, "image")


@app.route("/analyze/audio", methods=["POST"])
def analyze_audio_upload():
    from multimodal.audio import analyze_audio
    return analyze_uploaded_file(analyze_audio, "audio")


# ==========================================
# EVIDENCE VAULT ENDPOINTS
# ==========================================

@app.route("/vault", methods=["GET"])
def vault_cases():
    result = get_cases()

    if not result["success"]:
        print("Evidence Vault fetch error:", result["error"])
        return jsonify({
            "success": False,
            "error": "Unable to load saved cases"
        }), 500

    return jsonify({
        "success": True,
        "cases": result["data"]
    }), 200


@app.route("/vault/<int:case_id>", methods=["GET"])
def vault_case(case_id):
    result = get_case(case_id)

    if not result["success"]:
        if result["error"] == "Case not found":
            return jsonify({
                "success": False,
                "error": "Case not found"
            }), 404

        print("Evidence Vault case fetch error:", result["error"])
        return jsonify({
            "success": False,
            "error": "Unable to load this saved case"
        }), 500

    return jsonify({
        "success": True,
        "case": result["data"]
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

    if indicators is None:
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
        # Keep a single predictable process by default. Set FLASK_DEBUG=1 only
        # when actively developing the backend and needing auto-reload.
        debug=os.getenv("FLASK_DEBUG") == "1",
        host="127.0.0.1",
        port=int(os.getenv("PORT", "5001"))
    )
