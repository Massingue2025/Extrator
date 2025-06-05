const { spawn } = require("child_process");
require("dotenv").config();
const http = require("http"); // Adicionado

const FB_STREAM_KEY = process.env.FB_STREAM_KEY;
const VIDEO_URL = process.env.VIDEO_URL;
const DURATION_MINUTES = parseInt(process.env.LIVE_DURATION_MINUTES || "30", 10);

if (!FB_STREAM_KEY || !VIDEO_URL) {
  console.error("❌ Erro: .env incompleto");
  process.exit(1);
}

const streamUrl = `rtmps://live-api-s.facebook.com:443/rtmp/${FB_STREAM_KEY}`;
const totalSeconds = DURATION_MINUTES * 60;

console.log(`🔴 Iniciando live por ${DURATION_MINUTES} minutos...`);

const ffmpegProcess = spawn("ffmpeg", [
  "-re",
  "-stream_loop", "-1",
  "-i", VIDEO_URL,
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

const startTime = Date.now();
const interval = setInterval(() => {
  const elapsed = (Date.now() - startTime) / 1000;
  if (elapsed >= totalSeconds) {
    console.log("⏹️ Live finalizada.");
    ffmpegProcess.kill("SIGINT");
    clearInterval(interval);
  }
}, 5000);

// ✅ Mínimo servidor para manter Render ativo
const PORT = process.env.PORT || 10000;
http.createServer((req, res) => {
  res.writeHead(200, { "Content-Type": "text/plain" });
  res.end("Servidor ativo. A live está rodando em segundo plano.\n");
}).listen(PORT, () => {
  console.log(`🌐 Servidor HTTP rodando na porta ${PORT}`);
});
