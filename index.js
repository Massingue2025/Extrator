const express = require('express');
const { create } = require('@wppconnect-team/wppconnect');
const bodyParser = require('body-parser');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();
const port = process.env.PORT || 3000;

app.use(cors());
app.use(bodyParser.json());
app.use(express.static(__dirname));

let client;

create({
  session: 'sessionZap',
  catchQR: (base64Qr) => {
    const base64Image = base64Qr.replace(/^data:image\/png;base64,/, "");
    fs.writeFileSync("qr.png", base64Image, 'base64');
    console.log("✅ QR code atualizado (qr.png).");
  },
  statusFind: (status) => console.log('🟢 Status:', status),
  headless: true,
  devtools: false,
  useChrome: true
}).then((_client) => {
  client = _client;
  console.log("✅ Cliente WhatsApp iniciado.");
});

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

app.post('/send-message', async (req, res) => {
  const { number, message } = req.body;

  if (!number || !message) {
    return res.status(400).json({ error: 'Número e mensagem obrigatórios.' });
  }

  try {
    await client.sendText(`${number}@c.us`, message);
    res.json({ status: '✅ Mensagem enviada!' });
  } catch (error) {
    res.status(500).json({ error: '❌ Erro ao enviar.', detail: error.message });
  }
});

app.listen(port, () => {
  console.log(`🚀 Servidor rodando em http://localhost:${port}`);
});
