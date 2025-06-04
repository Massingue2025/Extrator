from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import subprocess
import os

app = FastAPI()

# Serve arquivos estáticos (como index.html)
app.mount("/static", StaticFiles(directory="."), name="static")

@app.get("/", response_class=HTMLResponse)
async def root():
    return FileResponse("index.html")

@app.post("/send")
async def send_message(number: str = Form(...), message: str = Form(...)):
    # Envia mensagem usando o client do WppConnect
    from wppconnect import WhatsApp
    client = WhatsApp()

    await client.send_message(phone=number, message=message)
    return {"status": "Mensagem enviada!"}
