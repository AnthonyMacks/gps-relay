from flask import Flask, request, jsonify
import requests
import logging
import os

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# 🌐 Render server endpoint (update to match your real URL)
RENDER_URL = "https://gps-tracker-69gb.onrender.com/gps"

def is_valid_gps(data):
    try:
        lat = float(data.get("latitude", 0))
        lon = float(data.get("longitude", 0))
        return lat != 0.0 and lon != 0.0
    except (ValueError, TypeError):
        return False

@app.route("/gps", methods=["POST"])
def relay():
    try:
        # 📨 Read JSON payload
        data = request.get_json(force=True)
        logging.info("📥 Received GPS from device: %s", data)
        print(f"📥 Received GPS from device: {data}")

        # ✅ Validate GPS data
        if not is_valid_gps(data):
            logging.warning("⚠️ Invalid GPS data received: %s", data)
            return jsonify({"error": "invalid GPS data"}), 400

        # 🔢 Convert types
        data["latitude"] = float(data["latitude"])
        data["longitude"] = float(data["longitude"])
        data["sats"] = int(data["sats"])

        # 🔁 Forward to Render
        response = requests.post(RENDER_URL, json=data, headers={"Content-Type": "application/json"})
        logging.info("🚀 Relayed to Render: %s (status %d)", response.text, response.status_code)

        return jsonify({"status": "relayed", "code": response.status_code}), response.status_code

    except Exception as e:
        logging.error("❌ Relay error: %s", str(e))
        return jsonify({"error": "bad request", "details": str(e)}), 400
@app.route("/", methods=["GET"])
def health():
    return "🟢 Fly relay is up and forwarding GPS data."

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=PORT)
