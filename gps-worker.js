import express from "express";
import http from "http";
import { Server as SocketIO } from "socket.io";
import bodyParser from "body-parser";

// Create Express and HTTP server
const app = express();
const server = http.createServer(app);
const io = new SocketIO(server, {
  cors: { origin: "*" }
});

// Buffer setup for graceful shutdown
let buffer = [];
let flushBuffer = true;

// Middleware
app.use(bodyParser.json());

// GPS endpoint
app.post("/gps", (req, res) => {
  const data = req.body;
  console.log("📡 Received GPS:", data);

  if (flushBuffer) {
    io.emit("gps_update", data);
  } else {
    buffer.push(data);
    console.log("⏸️ Buffering GPS packet during shutdown");
  }

  res.send({ status: "received" });
});

// Graceful shutdown handler
process.on("SIGTERM", () => {
  flushBuffer = false;
  console.log("🛑 SIGTERM received: flushing GPS buffer...");

  buffer.forEach((entry) => {
    io.emit("gps_update", entry);
  });

  console.log(`✅ Flushed ${buffer.length} buffered entries`);
  process.exit(0);
});

// Bind to Fly.io's assigned port
const PORT = process.env.PORT || 4000;
server.listen(PORT, () => {
  console.log(`🚀 GPS Worker running on port ${PORT}`);
});
