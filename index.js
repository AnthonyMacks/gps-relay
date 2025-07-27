import express from "express";
import fetch from "node-fetch"; // Ensure this is installed via `npm install node-fetch`

const app = express();
app.use(express.json());

console.log("🧪 TEST LOG: Deployed code is active.");

// 🛰️ Simple status route
app.get("/", (req, res) => {
  res.send("🛰️ GPS Relay Server is running. POST GPS data to /relay.");
});

// 🔁 GPS relay endpoint
app.post("/relay", async (req, res) => {
  const gpsData = req.body;

  // 📝 Log incoming data with timestamp
  console.log(`[${new Date().toISOString()}] 📥 Received GPS data:`, gpsData);

  if (!gpsData || !gpsData.latitude || !gpsData.longitude || !gpsData.device_id) {
    console.warn(`[${new Date().toISOString()}] ⚠️ Invalid GPS payload:`, gpsData);
    return res.status(400).send({ error: "Invalid GPS data" });
  }

  try {
    const response = await fetch("https://gps-tracker-69gb.onrender.com/gps", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(gpsData),
    });

    const result = await response.text(); // Use .json() if you expect JSON
    console.log(`[${new Date().toISOString()}] ✅ Relayed to Render:`, gpsData);

    res.status(200).send(result);
  } catch (err) {
    console.error(`[${new Date().toISOString()}] ❌ Relay error:`, err.message || err);
    res.status(500).send({ error: "Relay failed", details: err.message });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`[${new Date().toISOString()}] 🚀 GPS Relay server running on port ${PORT}`);
});
