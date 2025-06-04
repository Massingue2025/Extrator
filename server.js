const express = require('express');
const cors = require('cors');
const { create } = require('@wppconnect-team/wppconnect');

const app = express();
app.use(cors());
app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(express.static('.')); // serve index.html

let client;

create()
  .then((wpp) => {
    client = wpp;
    console.log("✅ Cliente WhatsApp conectado.");
  })
  .catch((error) => console.error("Erro ao iniciar o cliente:", error));

app.post('/send', async (req, res) => {
  const { number, message } = req.body;
  try {
    await client.sendText(number + '@c.us', message);
    res.json({ status: 'Mensagem enviada com sucesso' });
  } catch (err) {
    res.status(500).json({ error: 'Erro ao enviar mensagem' });
  }
});

app.listen(3000, () => {
  console.log('🚀 Servidor rodando na porta 3000');
});
