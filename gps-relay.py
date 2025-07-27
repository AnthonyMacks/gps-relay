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
        # Relaxed validation: allow 0.0 but log a warning
        if lat == 0.0 and lon == 0.0:
            logging.warning("⚠️ GPS coordinates are both zero.")
        return True
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

        # 🔢 Convert types safely
        try:
            data["latitude"] = float(data.get("latitude", 0.0))
            data["longitude"] = float(data.get("longitude", 0.0))
            data["sats"] = int(data.get("sats", 0))
        except (ValueError, TypeError) as e:
            logging.warning("⚠️ Type conversion failed: %s", str(e))
            return jsonify({"error": "invalid data format"}), 400

        # 🔁 Forward to Render with timeout
        try:
            response = requests.post(RENDER_URL, json=data, headers={"Content-Type": "application/json"}, timeout=5)
            logging.info("🚀 Relayed to Render: %s (status %d)", response.text, response.status_code)
        except requests.exceptions.RequestException as e:
            logging.error("❌ Failed to forward to Render: %s", str(e))
            return jsonify({"error": "forwarding failed", "details": str(e)}), 502

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

