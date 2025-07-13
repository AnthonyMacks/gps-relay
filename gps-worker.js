import express from "express";
import http from "http";
import { Server as SocketIO } from "socket.io";
import bodyParser from "body-parser";

// 🚀 Create Express and HTTP server
const app = express();
const server = http.createServer(app);
const io = new SocketIO(server, {
  cors: { origin: "*" }
});

// 📦 Buffer setup for graceful shutdown
let buffer = [];
let flushBuffer = true;

// 🛠️ Middleware
app.use(bodyParser.json());

// 🌐 Status route
app.get("/", (req, res) => {
  res.send("🧭 GPS Worker is online and broadcasting GPS updates.");
});

// 📡 GPS endpoint: receive + emit
app.post("/gps", (req, res) => {
  const data = req.body;

  if (!data || !data.latitude || !data.longitude || !data.device_id) {
    console.warn("⚠️ Invalid GPS payload:", data);
    return res.status(400).send({ error: "Invalid GPS data" });
  }

  console.log("📡 Received GPS:", data);

  if (flushBuffer) {
    io.emit("gps_update", data);
    console.log("📤 Emitted GPS to dashboard:", data);
  } else {
    buffer.push(data);
    console.log("⏸️ Buffering GPS packet during shutdown");
  }

  res.send({ status: "received" });
});

// 🧹 Graceful shutdown handler
process.on("SIGTERM", () => {
  flushBuffer = false;
  console.log("🛑 SIGTERM received: flushing GPS buffer...");

  buffer.forEach((entry) => {
    io.emit("gps_update", entry);
  });

  console.log(`✅ Flushed ${buffer.length} buffered entries`);
  process.exit(0);
});

// 🔉 Bind to Fly.io-assigned port
const PORT = process.env.PORT || 4000;
server.listen(PORT, () => {
  console.log(`🚀 GPS Worker running on port ${PORT}`);
});
