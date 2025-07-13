// test-server.js
import express from "express";
const app = express();
app.get("/", (req, res) => res.send("Hello from 4000"));
app.listen(4000, () => console.log("Test server on port 4000"));