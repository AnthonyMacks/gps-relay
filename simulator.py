# GPS Simulator - Improvements & Testing Guide

## 🎯 **Current Issues to Fix**

### 1. **Timestamp Format Mismatch**
**Problem:** Your simulator sends timestamps as `"2025-01-28T12:00:00"` but your `app.py` expects `"2025-01-28 12:00:00"` (space instead of T).

**Fix in simulator.py:**
```python
# Change this line:
timestamp = time.strftime("%Y-%m-%dT%H:%M:%S")
# To this:
timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
```

### 2. **Missing Satellite Data**
Your map shows satellite count, but simulator doesn't send it.

**Add to build_packet():**
```python
def build_packet(device_id):
    lat, lon = generate_point(SYDNEY_LAT, SYDNEY_LON)
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")  # ← Fixed format
    return {
        "device_id": device_id,
        "latitude": str(lat),
        "longitude": str(lon),
        "timestamp": timestamp,
        "sats": random.randint(4, 12)  # ← Add realistic satellite count
    }
```

### 3. **URL Configuration**
Make sure your `RELAY_URL` points to your actual Fly.io deployment:
```python
RELAY_URL = "https://YOUR-ACTUAL-FLY-APP.fly.dev/gps"
```

## 🚀 **Enhanced Simulator Version**

Here's an improved version with better error handling and realistic movement:

```python
import time, random, json, requests
from datetime import datetime

# 🌏 Sydney CBD coordinates
SYDNEY_LAT = -33.8688
SYDNEY_LON = 151.2093

# 🎯 Movement parameters
MAX_LAT_OFFSET = 0.0135  # ~1.5km spread
MAX_LON_OFFSET = 0.0180
MOVEMENT_STEP = 0.0001   # Small steps for realistic movement

# 🆔 Test devices
DEVICE_IDS = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X']

# 🌐 Endpoints
RELAY_URL = "https://gps-relay.fly.dev/gps"  # Your Fly.io relay
DIRECT_URL = "https://your-render-app.onrender.com/gps"  # Direct to Render (for testing)

# 📍 Track current positions for realistic movement
device_positions = {}

def initialize_positions():
    """Give each device a random starting position"""
    for device_id in DEVICE_IDS:
        lat = SYDNEY_LAT + random.uniform(-MAX_LAT_OFFSET, MAX_LAT_OFFSET)
        lon = SYDNEY_LON + random.uniform(-MAX_LON_OFFSET, MAX_LON_OFFSET)
        device_positions[device_id] = [round(lat, 6), round(lon, 6)]
    print(f"🎲 Initialized {len(device_positions)} device positions")

def move_device(device_id):
    """Move device slightly from current position (realistic movement)"""
    if device_id not in device_positions:
        initialize_positions()
    
    current_lat, current_lon = device_positions[device_id]
    
    # Small random movement
    new_lat = current_lat + random.uniform(-MOVEMENT_STEP, MOVEMENT_STEP)
    new_lon = current_lon + random.uniform(-MOVEMENT_STEP, MOVEMENT_STEP)
    
    # Keep within Sydney bounds
    new_lat = max(SYDNEY_LAT - MAX_LAT_OFFSET, min(SYDNEY_LAT + MAX_LAT_OFFSET, new_lat))
    new_lon = max(SYDNEY_LON - MAX_LON_OFFSET, min(SYDNEY_LON + MAX_LON_OFFSET, new_lon))
    
    device_positions[device_id] = [round(new_lat, 6), round(new_lon, 6)]
    return new_lat, new_lon

def build_packet(device_id):
    """Build GPS packet with realistic data"""
    lat, lon = move_device(device_id)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return {
        "device_id": device_id,
        "latitude": str(lat),
        "longitude": str(lon),
        "timestamp": timestamp,
        "sats": random.randint(4, 12),  # Realistic satellite count
        "speed": round(random.uniform(0, 60), 1),  # Optional: speed in km/h
        "heading": random.randint(0, 359)  # Optional: compass heading
    }

def send_packet(packet, use_direct=False):
    """Send packet via relay or directly to Render"""
    url = DIRECT_URL if use_direct else RELAY_URL
    route = "direct" if use_direct else "relay"
    
    try:
        response = requests.post(url, json=packet, timeout=10)
        status = "✅" if response.status_code == 200 else "⚠️"
        print(f"{status} [{route}] {packet['device_id']} → ({packet['latitude']}, {packet['longitude']}) | {packet['sats']} sats | {response.status_code}")
        return response.status_code == 200
    except requests.exceptions.Timeout:
        print(f"⏰ [{route}] Timeout for {packet['device_id']}")
        return False
    except Exception as e:
        print(f"❌ [{route}] Failed {packet['device_id']} → {str(e)}")
        return False

def test_endpoints():
    """Test both relay and direct endpoints"""
    print("🧪 Testing endpoints...")
    test_packet = build_packet("TEST")
    
    print("Testing relay endpoint...")
    relay_ok = send_packet(test_packet, use_direct=False)
    
    print("Testing direct endpoint...")
    direct_ok = send_packet(test_packet, use_direct=True)
    
    if not relay_ok and not direct_ok:
        print("❌ Both endpoints failed! Check your URLs.")
        return False
    
    return True

def run_simulator(interval=10, use_direct=False):
    """Run the GPS simulator"""
    initialize_positions()
    
    if not test_endpoints():
        print("🛑 Endpoint test failed. Exiting.")
        return
    
    mode = "direct to Render" if use_direct else "via Fly.io relay"
    print(f"🚀 GPS simulator running ({mode})... Ctrl+C to stop.")
    print(f"📡 Sending data every {interval} seconds for {len(DEVICE_IDS)} devices")
    
    packet_count = 0
    
    try:
        while True:
            start_time = time.time()
            
            for device_id in DEVICE_IDS:
                packet = build_packet(device_id)
                send_packet(packet, use_direct)
                packet_count += 1
                time.sleep(0.1)  # Small delay between devices
            
            elapsed = time.time() - start_time
            sleep_time = max(0, interval - elapsed)
            
            print(f"📊 Batch complete. {packet_count} total packets sent. Sleeping {sleep_time:.1f}s...")
            time.sleep(sleep_time)
            
    except KeyboardInterrupt:
        print(f"\n🛑 Simulator stopped. Sent {packet_count} total packets.")

if __name__ == "__main__":
    import sys
    
    # Command line options
    interval = 10
    use_direct = False
    
    if len(sys.argv) > 1:
        if "direct" in sys.argv:
            use_direct = True
        if "fast" in sys.argv:
            interval = 3
        if "slow" in sys.argv:
            interval = 30
    
    run_simulator(interval, use_direct)
```

## 🧪 **Testing Commands**

Run these from your GitBash:

```bash
# Normal testing (via Fly.io relay)
python simulator.py

# Fast testing (3 second intervals)
python simulator.py fast

# Direct to Render (bypass relay)
python simulator.py direct

# Direct + fast testing
python simulator.py direct fast
```

## 🔍 **Debugging Steps**

### 1. **Test Individual Components:**

**Test your Fly.io relay:**
```bash
curl -X POST https://your-fly-app.fly.dev/gps \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "CURL_TEST",
    "latitude": "-33.8688",
    "longitude": "151.2093", 
    "timestamp": "2025-01-28 12:00:00",
    "sats": 8
  }'
```

**Test your Render server directly:**
```bash
curl -X POST https://your-render-app.onrender.com/gps \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "DIRECT_TEST",
    "latitude": "-33.8688",
    "longitude": "151.2093",
    "timestamp": "2025-01-28 12:00:00", 
    "sats": 8
  }'
```

### 2. **Monitor Your Map:**
- Open your Render app URL in browser
- Watch the debug panel for connection status
- Check browser console for WebSocket messages
- Look for new markers appearing on the map

### 3. **Check Logs:**
- **Render logs**: Check your Render dashboard for incoming requests
- **Fly.io logs**: Use `flyctl logs` to see relay activity
- **Simulator output**: Watch for HTTP status codes

## 🎯 **Expected Results:**

When working correctly, you should see:
1. **Simulator**: `✅ [relay] I → (-33.868234, 151.209876) | 8 sats | 200`
2. **Browser map**: New colored dots appearing for each device
3. **Data table**: Updating with latest coordinates and packet counts
4. **Debug panel**: Shows increasing device/point counts

The simulator creates realistic movement patterns, so you'll see devices "walking" around Sydney rather than jumping randomly!
