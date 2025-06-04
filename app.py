from flask import Flask, request, send_file
from io import BytesIO
from PIL import Image
import os
import subprocess

app = Flask(__name__)

@app.route('/', methods=['POST'])
def enhance_image():
    if 'image' not in request.files:
        return "Imagem não enviada", 400

    image_file = request.files['image']
    scale = request.form.get('scale', '2')
    scale = scale if scale in ['2', '4'] else '2'

    input_path = 'input.png'
    output_path = 'output.png'

    # Salva imagem temporária
    image = Image.open(image_file)
    image.save(input_path)

    # Executa Real-ESRGAN com o modelo real
    command = [
        './realesrgan-ncnn-vulkan',
        '-i', input_path,
        '-o', output_path,
        '-s', scale
    ]

    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        return f"Erro ao melhorar a imagem: {result.stderr.decode()}", 500

    with open(output_path, 'rb') as f:
        img_bytes = BytesIO(f.read())

    # Limpa arquivos temporários
    os.remove(input_path)
    os.remove(output_path)

    return send_file(img_bytes, mimetype='image/png')

@app.route('/', methods=['GET'])
def home():
    return "Servidor de melhoria de imagem com IA. Envie via POST com 'image' e 'scale'."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
