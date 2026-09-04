from flask import Flask, request, jsonify
from flask_cors import CORS

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


if __name__ == "__main__":
    app.run(debug=True)