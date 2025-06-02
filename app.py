from flask import Flask, request, jsonify
from flask_cors import CORS
import easyocr
from PIL import Image
import numpy as np

app = Flask(__name__)
CORS(app)

reader = easyocr.Reader(['pt', 'en'])  # Idiomas português e inglês

@app.route('/extrair-texto', methods=['POST'])
def extrair_texto():
    if 'imagem' not in request.files:
        return jsonify({'error': 'Nenhuma imagem enviada'}), 400

    imagem = request.files['imagem']
    try:
        img = Image.open(imagem.stream).convert('RGB')
        img_np = np.array(img)
        resultado = reader.readtext(img_np, detail=0)
        texto = '\n'.join(resultado)
        return jsonify({'texto': texto})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
