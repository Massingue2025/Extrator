const express = require('express');
const { create } = require('@wppconnect-team/wppconnect');
const bodyParser = require('body-parser');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();
const port = 3000;
let client;

app.use(cors());
app.use(bodyParser.json());
app.use(express.static(__dirname));

create({
  session: 'sessaoZap',
  catchQR: (base64Qr) => {
    const base64Image = base64Qr.replace(/^data:image\/png;base64,/, '');
    fs.writeFileSync('qr.png', base64Image, 'base64');
    console.log('📲 Escaneie o QR code no navegador!');
  },
  headless: true,
  statusFind: (status) => console.log('Status:', status)
}).then((_client) => {
  client = _client;
  console.log('✅ WhatsApp conectado com sucesso!');
});

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

app.post('/send-message', async (req, res) => {
  const { number, message } = req.body;
  if (!number || !message) return res.status(400).json({ error: 'Número e mensagem obrigatórios.' });

  try {
    await client.sendText(`${number}@c.us`, message);
    res.json({ status: '✅ Mensagem enviada!' });
  } catch (e) {
    res.status(500).json({ error: '❌ Falha ao enviar.', detail: e.message });
  }
});

app.listen(port, () => {
  console.log(`🌐 Acesse: http://localhost:${port}`);
});
