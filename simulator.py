import time, random, json, requests

# 🌏 Center on Sydney CBD
SYDNEY_LAT = -32.7585
SYDNEY_LON = 151.1745

# 🎯 Spread radius (~1.5km)
MAX_LAT_OFFSET = 0.02
MAX_LON_OFFSET = 0.02

# 🆔 Test devices
DEVICE_IDS = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X']

# 🌐 Fly.io GPS relay endpoint
RELAY_URL = "https://gps-relay.fly.dev/relay"

def generate_point(center_lat, center_lon):
    lat = round(center_lat + random.uniform(-MAX_LAT_OFFSET, MAX_LAT_OFFSET), 6)
    lon = round(center_lon + random.uniform(-MAX_LON_OFFSET, MAX_LON_OFFSET), 6)
    return lat, lon

def build_packet(device_id):
    lat, lon = generate_point(SYDNEY_LAT, SYDNEY_LON)
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")  # Fixed format (space instead of T)
    return {
        "device_id": device_id,
        "latitude": str(lat),
        "longitude": str(lon),
        "timestamp": timestamp,
        "sats": random.randint(4, 12)  # Added satellite count
    }

def send_packet(packet):
    try:
        response = requests.post(RELAY_URL, json=packet)
        print(f"SUCCESS: Sent {packet['device_id']} at {packet['latitude']}, {packet['longitude']} (status: {response.status_code})")
    except Exception as e:
        print(f"ERROR: Failed to send - {e}")

def run_simulator(interval=10):
    while True:
        for device_id in DEVICE_IDS:
            packet = build_packet(device_id)
            send_packet(packet)
        time.sleep(interval)

if __name__ == "__main__":
    print("GPS simulator running... Ctrl+C to stop.")
    run_simulator()
