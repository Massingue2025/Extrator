FROM python:3.10-slim

# Instalar Tesseract
RUN apt-get update && apt-get install -y tesseract-ocr

# Instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . /app
WORKDIR /app

# Porta padrão do Flask
EXPOSE 10000

CMD ["python", "app.py"]

