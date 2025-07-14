import time, random, json, requests

# 🌏 Center on Sydney CBD
SYDNEY_LAT = -33.8688
SYDNEY_LON = 151.2093

# 🎯 Spread radius (~1.5km)
MAX_LAT_OFFSET = 0.0135
MAX_LON_OFFSET = 0.0180

# 🆔 Test devices
DEVICE_IDS = ["I", "II"]

# 🌐 Fly.io GPS relay endpoint
RELAY_URL = "https://your-relay.fly.dev/gps"  # ← Replace with your actual endpoint

def generate_point(center_lat, center_lon):
    lat = round(center_lat + random.uniform(-MAX_LAT_OFFSET, MAX_LAT_OFFSET), 6)
    lon = round(center_lon + random.uniform(-MAX_LON_OFFSET, MAX_LON_OFFSET), 6)
    return lat, lon

def build_packet(device_id):
    lat, lon = generate_point(SYDNEY_LAT, SYDNEY_LON)
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%S")
    return {
        "device_id": device_id,
        "latitude": str(lat),
        "longitude": str(lon),
        "timestamp": timestamp
    }

def send_packet(packet):
    try:
        response = requests.post(RELAY_URL, json=packet)
        print(f"✅ Sent → {packet['device_id']} @ {packet['latitude']}, {packet['longitude']} ({response.status_code})")
    except Exception as e:
        print(f"⚠️ Failed → {e}")

def run_simulator(interval=10):
    while True:
        for device_id in DEVICE_IDS:
            packet = build_packet(device_id)
            send_packet(packet)
        time.sleep(interval)

if __name__ == "__main__":
    print("🚀 GPS simulator running... Ctrl+C to stop.")
    run_simulator()
