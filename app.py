import requests
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Webhook Route to Accept Incoming Requests
@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "success", "message": "Webhook is running"}), 200

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.json
        post_text = data.get("post_text", "")
        post_id = data.get("post_id", "")

        if not post_text or not post_id:
            return jsonify({"status": "error", "message": "Missing post_text or post_id"}), 400

        # Since you don't have a Devi API Key, we'll just return success.
        print(f"Received Post: {post_text} | Post ID: {post_id}")

        return jsonify({"status": "success", "message": "Webhook received successfully"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
