const express = require("express");
const multer = require("multer");
const { spawn } = require("child_process");
const fs = require("fs");
require("dotenv").config();

const app = express();
const upload = multer({ storage: multer.memoryStorage() });

app.use(express.static("public"));

app.post("/upload", upload.single("video"), async (req, res) => {
  const durationMin = parseInt(req.body.duration);
  if (!req.file || !durationMin || durationMin <= 0) {
    return res.status(400).send("Dados inválidos.");
  }

  const streamUrl = `rtmps://live-api-s.facebook.com:443/rtmp/${process.env.FB_STREAM_KEY}`;
  const totalSeconds = durationMin * 60;
  const tempPath = `/tmp/uploaded_${Date.now()}.mp4`;

  fs.writeFileSync(tempPath, req.file.buffer);

  const repeatStream = () => {
    return spawn("ffmpeg", [
      "-re",
      "-stream_loop", "-1",
      "-i", tempPath,
      "-c:v", "libx264",
      "-preset", "veryfast",
      "-maxrate", "3000k",
      "-bufsize", "6000k",
      "-pix_fmt", "yuv420p",
      "-g", "50",
      "-c:a", "aac",
      "-b:a", "128k",
      "-f", "flv",
      streamUrl
    ], { stdio: "inherit" });
  };

  const startTime = Date.now();
  const process = repeatStream();

  const interval = setInterval(() => {
    const elapsed = (Date.now() - startTime) / 1000;
    if (elapsed >= totalSeconds) {
      process.kill("SIGINT");
      clearInterval(interval);
      fs.unlinkSync(tempPath);
      console.log("Live finalizada.");
    }
  }, 5000);

  res.send("Live iniciada com sucesso no Facebook!");
});

const PORT = process.env.PORT || 10000;
app.listen(PORT, () => {
  console.log(`Servidor rodando na porta ${PORT}`);
});
