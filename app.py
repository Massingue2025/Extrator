from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import pytesseract
import io

app = Flask(__name__)
CORS(app)

@app.route('/extrair-texto', methods=['POST'])
def extrair_texto():
    if 'imagem' not in request.files:
        return jsonify({'error': 'Nenhuma imagem enviada'}), 400

    imagem = request.files['imagem']
    try:
        img = Image.open(imagem.stream)
        texto = pytesseract.image_to_string(img, lang='por+eng')  # Português e inglês
        return jsonify({'texto': texto.strip()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
