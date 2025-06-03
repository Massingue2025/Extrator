from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import subprocess
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder='.')  # templates na pasta atual

UPLOAD_FOLDER = 'uploads'
ENHANCED_FOLDER = 'enhanced'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'tiff'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(ENHANCED_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ENHANCED_FOLDER'] = ENHANCED_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def enhance_image(input_path, output_path, quality):
    # Map quality string para escala de ffmpeg
    # Usaremos escala de escala (scale), 140p até 4k
    quality_map = {
        '140': 140,
        '240': 240,
        '360': 360,
        '480': 480,
        '720': 720,
        '1080': 1080,
        '1440': 1440,
        '2160': 2160,  # 4K
    }
    height = quality_map.get(quality, 720)  # padrão 720p se inválido

    # Comando ffmpeg para upscale com Lanczos (melhor qualidade)
    command = [
        'ffmpeg',
        '-i', input_path,
        '-vf', f'scale=-2:{height}:flags=lanczos',
        '-q:v', '2',  # qualidade de saída (2 = alta qualidade)
        output_path,
        '-y'  # sobrescrever saída se existir
    ]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    enhanced_image = None
    if request.method == 'POST':
        if 'image' not in request.files:
            return "Nenhum arquivo enviado", 400
        file = request.files['image']
        quality = request.form.get('quality')
        if file.filename == '':
            return "Nenhum arquivo selecionado", 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(input_path)

            # Nome da imagem melhorada
            name, ext = os.path.splitext(filename)
            enhanced_filename = f"{name}_enhanced_{quality}{ext}"
            enhanced_path = os.path.join(app.config['ENHANCED_FOLDER'], enhanced_filename)

            try:
                enhance_image(input_path, enhanced_path, quality)
                enhanced_image = enhanced_filename
            except subprocess.CalledProcessError as e:
                return f"Erro ao processar imagem: {e}", 500

    return render_template('index.html', enhanced_image=enhanced_image)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/enhanced/<filename>')
def enhanced_file(filename):
    return send_from_directory(app.config['ENHANCED_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81, debug=True)
