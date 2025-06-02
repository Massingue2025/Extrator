from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import pytesseract

app = Flask(__name__)
CORS(app)

@app.route('/extrair-texto', methods=['POST'])
def extrair_texto():
    if 'imagem' not in request.files:
        return jsonify({'error': 'Nenhuma imagem enviada'}), 400

    imagem = request.files['imagem']

    try:
        img = Image.open(imagem.stream)
        texto = pytesseract.image_to_string(img)
        return jsonify({'texto': texto})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
