// gps-worker.js
const express = require("express");
const http = require("http");
const socketIO = require("socket.io");
const bodyParser = require("body-parser");

const app = express();
const server = http.createServer(app);
const io = socketIO(server, {
  cors: { origin: "*" }
});

let buffer = [];
let flushBuffer = true;
app.use(bodyParser.json());

app.post("/gps", (req, res) => {
  const data = req.body;
  console.log("📡 Received GPS:", data);

  if (flushBuffer) {
    io.emit("gps_update", data);
  } else {
    buffer.push(data);
    console.log("⏸️ Buffering packet");
  }

  res.send({ status: "received" });
});

process.on("SIGTERM", () => {
  flushBuffer = false;
  console.log("🛑 SIGTERM: Flushing buffer...");
  buffer.forEach((entry) => io.emit("gps_update", entry));
  process.exit(0);
});

const PORT = process.env.PORT || 4000;
server.listen(PORT, () => {
  console.log(`🚀 GPS Worker running on port ${PORT}`);
});
