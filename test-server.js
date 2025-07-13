<<<<<<< HEAD
// test-server.js
import express from "express";
const app = express();
app.get("/", (req, res) => res.send("Hello from 4000"));
=======
// test-server.js
import express from "express";
const app = express();
app.get("/", (req, res) => res.send("Hello from 4000"));
>>>>>>> 6ea2398 (Initial project setup with relay, map, worker, and supporting files)
app.listen(4000, () => console.log("Test server on port 4000"));