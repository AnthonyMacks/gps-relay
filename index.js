import express from "express";

const app = express();
app.use(express.json());

app.post("/relay", async (req, res) => {
  try {
    const response = await fetch("https://gps-tracker-69gb.onrender.com/gps", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(req.body)
    });

    const result = await response.text(); // Adjust this to .json() if needed
    console.log("✅ Relayed:", req.body);
    res.status(200).send(result);
  } catch (err) {
    console.error("❌ Relay error:", err);
    res.status(500).send({ error: "Relay failed" });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`🚀 Relay server running on port ${PORT}`);
});
