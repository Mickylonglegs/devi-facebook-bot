import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS

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

        print(f"Received Post: {post_text} | Post ID: {post_id}")

        response = jsonify({"status": "success", "message": "Webhook received successfully"})
        response.headers["Content-Type"] = "application/json"  # Ensure correct response format
        return response, 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Correct way to bind dynamic port
    app.run(host="0.0.0.0", port=port, debug=True)
