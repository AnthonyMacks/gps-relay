<<<<<<< HEAD
from flask import Flask, request, jsonify
import requests
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# 🌐 Your Render server (HTTPS endpoint)
RENDER_URL = "https://your-render-app.onrender.com/gps"

@app.route("/gps", methods=["POST"])
def relay():
    try:
        # 📨 Read raw JSON payload from device
        data = request.get_json(force=True)
        logging.info("📥 Received GPS from device: %s", data)

        # 🔁 Forward to Render securely
        response = requests.post(RENDER_URL, json=data, headers={"Content-Type": "application/json"})
        logging.info("🚀 Relayed to Render: %s (status %d)", response.text, response.status_code)

        return jsonify({"status": "relayed", "code": response.status_code})

    except Exception as e:
        logging.error("❌ Relay error: %s", str(e))
        return jsonify({"error": "bad request", "details": str(e)}), 400

@app.route("/", methods=["GET"])
def health():
    return "🟢 Fly relay is up and forwarding GPS data."

if __name__ == "__main__":
=======
from flask import Flask, request, jsonify
import requests
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# 🌐 Your Render server (HTTPS endpoint)
RENDER_URL = "https://your-render-app.onrender.com/gps"

@app.route("/gps", methods=["POST"])
def relay():
    try:
        # 📨 Read raw JSON payload from device
        data = request.get_json(force=True)
        logging.info("📥 Received GPS from device: %s", data)

        # 🔁 Forward to Render securely
        response = requests.post(RENDER_URL, json=data, headers={"Content-Type": "application/json"})
        logging.info("🚀 Relayed to Render: %s (status %d)", response.text, response.status_code)

        return jsonify({"status": "relayed", "code": response.status_code})

    except Exception as e:
        logging.error("❌ Relay error: %s", str(e))
        return jsonify({"error": "bad request", "details": str(e)}), 400

@app.route("/", methods=["GET"])
def health():
    return "🟢 Fly relay is up and forwarding GPS data."

if __name__ == "__main__":
>>>>>>> 6ea2398 (Initial project setup with relay, map, worker, and supporting files)
    app.run(host="0.0.0.0", port=8080)