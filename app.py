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

        # Ensure data has 'items' and at least one item
        if not data or "items" not in data or len(data["items"]) == 0:
            return jsonify({"status": "error", "message": "Invalid data format"}), 400
        
        # Extract the first post's content and ID
        first_item = data["items"][0]
        post_text = first_item.get("content", "")
        post_id = first_item.get("id", "")

        # Validate received data
        if not post_text or not post_id:
            return jsonify({"status": "error", "message": "Missing post_text or post_id"}), 400

        print(f"Received Post: {post_text} | Post ID: {post_id}")

        return jsonify({"status": "success", "message": "Webhook received successfully"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Correct dynamic port handling
    app.run(host="0.0.0.0", port=port, debug=True)
