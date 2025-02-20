import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# ✅ Route to check if the webhook is running
@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "success", "message": "Webhook is running"}), 200

# ✅ Main webhook to process Devi AI requests
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.json  # Receive the data from Devi AI
        items = data.get("items", [])

        if not items:
            return jsonify({"status": "error", "message": "No items received"}), 400

        for item in items:
            post_id = item.get("id", "")
            post_text = item.get("content", "")

            if not post_id or not post_text:
                continue  # Skip invalid posts

            print(f"✅ Received Post: {post_text} | Post ID: {post_id}")

            # 🔹 Step 1: Ask Devi AI to generate a comment
            devi_response = requests.post(
                "https://devi-ai-url.com/generate-comment",  # Replace with actual Devi AI API
                json={"post_text": post_text},
                headers={"Authorization": f"Bearer {os.getenv('DEVI_API_KEY')}"}
            )

            if devi_response.status_code != 200:
                return jsonify({"status": "error", "message": "Failed to generate comment"}), 500

            generated_comment = devi_response.json().get("comment", "")

            # 🔹 Step 2: Post the comment to Facebook
            fb_response = requests.post(
                f"https://graph.facebook.com/v17.0/{post_id}/comments",
                json={"message": generated_comment},
                headers={"Authorization": f"Bearer {os.getenv('FACEBOOK_ACCESS_TOKEN')}"}
            )

            if fb_response.status_code == 200:
                print(f"✅ Comment Posted: {generated_comment}")
                return jsonify({"status": "success", "message": "Comment posted"}), 200
            else:
                return jsonify({"status": "error", "message": "Failed to post comment"}), 500

        return jsonify({"status": "success", "message": "Webhook processed"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Use dynamic port
    app.run(host="0.0.0.0", port=port, debug=True)
    
