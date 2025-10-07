import time, random, json, requests

# 🌏 Center on Maranagaroo Military Training Area - NAVEX
SYDNEY_LAT = -33.4452
SYDNEY_LON = 150.1528

# 🎯 Spread radius for VALID data (~4km - within 5km limit)
VALID_LAT_OFFSET = 0.035
VALID_LON_OFFSET = 0.035

# 💥 Spread radius for INVALID data (>5km to trigger rejection)
INVALID_LAT_OFFSET = 0.08
INVALID_LON_OFFSET = 0.08

# 🆔 Test devices
DEVICE_IDS = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 
              'XIII', 'XIV', 'XV', 'XVI', 'XVII', 'XVIII', 'XIX', 'XX', 'XXI', 'XXII', 
              'XXIII', 'XXIV', 'XXV', 'XXVI', 'XXVII', 'XXVIII', 'XXIX', 'XXX']

# 🌐 Fly.io GPS relay endpoint
RELAY_URL = "https://gps-relay.fly.dev/relay"

# 🎲 Percentage of invalid data to generate (0-100)
INVALID_DATA_PERCENTAGE = 20  # 20% of packets will be invalid

def generate_valid_point(center_lat, center_lon):
    """Generate point within ~4km of center (will pass 5km validation)"""
    lat = round(center_lat + random.uniform(-VALID_LAT_OFFSET, VALID_LAT_OFFSET), 6)
    lon = round(center_lon + random.uniform(-VALID_LON_OFFSET, VALID_LON_OFFSET), 6)
    return lat, lon

def generate_invalid_point(center_lat, center_lon):
    """Generate point >5km from center (will be rejected)"""
    lat = round(center_lat + random.uniform(-INVALID_LAT_OFFSET, INVALID_LAT_OFFSET), 6)
    lon = round(center_lon + random.uniform(-INVALID_LON_OFFSET, INVALID_LON_OFFSET), 6)
    return lat, lon

def generate_bad_coordinates():
    """Generate completely invalid coordinates"""
    invalid_types = [
        (999.999, 999.999),  # Out of range
        (-91.0, 181.0),       # Out of bounds
        (0.0, 0.0),           # Null island
        (None, None),         # Null values
    ]
    return random.choice(invalid_types)

def build_packet(device_id):
    """Build GPS packet - can be valid or invalid based on percentage"""
    
    # Decide if this packet should be invalid
    is_invalid = random.randint(1, 100) <= INVALID_DATA_PERCENTAGE
    
    if is_invalid:
        # Choose type of invalid data
        invalid_type = random.choice(['far_distance', 'bad_coords', 'low_sats', 'missing_field'])
        
        if invalid_type == 'far_distance':
            # Point beyond 5km limit
            lat, lon = generate_invalid_point(SYDNEY_LAT, SYDNEY_LON)
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            packet = {
                "device_id": device_id,
                "latitude": str(lat),
                "longitude": str(lon),
                "timestamp": timestamp,
                "sats": random.randint(1, 20)
            }
            print(f"🚫 INVALID (>5km): {device_id}")
            
        elif invalid_type == 'bad_coords':
            # Completely invalid coordinates
            lat, lon = generate_bad_coordinates()
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            packet = {
                "device_id": device_id,
                "latitude": str(lat) if lat is not None else "NaN",
                "longitude": str(lon) if lon is not None else "NaN",
                "timestamp": timestamp,
                "sats": random.randint(5, 12)
            }
            print(f"🚫 INVALID (bad coords): {device_id}")
            
        elif invalid_type == 'low_sats':
            # Low satellite count (< 4 triggers warning)
            lat, lon = generate_valid_point(SYDNEY_LAT, SYDNEY_LON)
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            packet = {
                "device_id": device_id,
                "latitude": str(lat),
                "longitude": str(lon),
                "timestamp": timestamp,
                "sats": random.randint(0, 3)  # Low sat count
            }
            print(f"⚠️  LOW SATS: {device_id} (sats={packet['sats']})")
            
        else:  # missing_field
            # Missing required field
            lat, lon = generate_valid_point(SYDNEY_LAT, SYDNEY_LON)
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            missing = random.choice(['latitude', 'longitude', 'timestamp'])
            packet = {
                "device_id": device_id,
                "latitude": str(lat),
                "longitude": str(lon),
                "timestamp": timestamp,
                "sats": random.randint(5, 12)
            }
            del packet[missing]  # Remove a required field
            print(f"🚫 INVALID (missing {missing}): {device_id}")
    
    else:
        # Generate VALID data
        lat, lon = generate_valid_point(SYDNEY_LAT, SYDNEY_LON)
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        packet = {
            "device_id": device_id,
            "latitude": str(lat),
            "longitude": str(lon),
            "timestamp": timestamp,
            "sats": random.randint(4, 12)
        }
        print(f"✅ VALID: {device_id} at {lat}, {lon}")
    
    return packet

def send_packet(packet):
    try:
        response = requests.post(RELAY_URL, json=packet)
        if response.status_code == 200:
            print(f"   → Sent successfully (status: {response.status_code})")
        else:
            print(f"   → Server response: {response.status_code}")
    except Exception as e:
        print(f"   → ERROR: Failed to send - {e}")

def run_simulator(interval=10, packets_per_cycle=5):
    """
    Run simulator with configurable settings
    
    Args:
        interval: Seconds between cycles (default 10)
        packets_per_cycle: Number of devices to update per cycle (default 5)
    """
    print(f"🚀 GPS Simulator Starting...")
    print(f"📍 Center: {SYDNEY_LAT}, {SYDNEY_LON}")
    print(f"🎯 Valid radius: ~4km, Invalid radius: ~7km")
    print(f"💥 Invalid data rate: {INVALID_DATA_PERCENTAGE}%")
    print(f"⏱️  Update interval: {interval}s")
    print(f"📦 Packets per cycle: {packets_per_cycle}")
    print(f"🔄 Total devices: {len(DEVICE_IDS)}")
    print("-" * 60)
    
    device_index = 0
    cycle = 0
    
    while True:
        cycle += 1
        print(f"\n📡 CYCLE {cycle} ({time.strftime('%H:%M:%S')})")
        print("-" * 60)
        
        # Send packets for next N devices
        for _ in range(packets_per_cycle):
            device_id = DEVICE_IDS[device_index]
            packet = build_packet(device_id)
            send_packet(packet)
            
            device_index = (device_index + 1) % len(DEVICE_IDS)
            time.sleep(0.5)  # Small delay between packets
        
        print("-" * 60)
        time.sleep(interval)

if __name__ == "__main__":
    print("🌟 Enhanced GPS Simulator with Valid & Invalid Data")
    print("Press Ctrl+C to stop.\n")
    
    # Configurable parameters
    try:
        run_simulator(
            interval=10,           # Send every 10 seconds
            packets_per_cycle=5    # Update 5 devices per cycle
        )
    except KeyboardInterrupt:
        print("\n\n✋ Simulator stopped by user")
