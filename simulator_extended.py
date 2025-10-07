import time, random, json, requests

# 🌏 Center on Ex Admin Bravo - NAVEX
SYDNEY_LAT = -33.4452
SYDNEY_LON = 150.1528

# 🎯 Spread radius (~1km)
MAX_LAT_OFFSET = 0.0067
MAX_LON_OFFSET = 0.0067

# 🆔 Test devices
DEVICE_IDS = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII', 'XVIII', 'XIX', 'XX', 'XXI', 'XXII', 'XXIII', 'XXIV', 'XXV', 'XXVI', 'XXVII' , 'XXVIII' , 'XXIX' , 'XXX']

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

def run_simulator(interval=60):
    while True:
        for device_id in DEVICE_IDS:
            packet = build_packet(device_id)
            send_packet(packet)
        time.sleep(interval)

if __name__ == "__main__":
    print("GPS simulator running... Ctrl+C to stop.")
    run_simulator()