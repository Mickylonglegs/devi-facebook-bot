@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.json  # Get full JSON data
        print("Received Data from Devi AI:", data)  # Debugging line

        # Extract first item from 'items' array (assuming only one post at a time)
        if "items" in data and isinstance(data["items"], list) and len(data["items"]) > 0:
            first_item = data["items"][0]  # Get first post
            
            post_text = first_item.get("content", "")  # Extract post content
            post_id = first_item.get("id", "")  # Extract post ID

            if not post_text or not post_id:
                return jsonify({"status": "error", "message": "Missing post content or post ID"}), 400

            print(f"Processed Post: {post_text} | Post ID: {post_id}")  # Log extracted values

            return jsonify({"status": "success", "message": "Webhook received successfully", "post_text": post_text, "post_id": post_id}), 200

        return jsonify({"status": "error", "message": "No valid items found in payload"}), 400

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
