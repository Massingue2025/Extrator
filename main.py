from flask import Flask, request, render_template_string, send_from_directory
import os
from PIL import Image
from realesrgan import RealESRGAN
import torch
import requests

app = Flask(__name__)
UPLOAD_FOLDER = 'static/enhanced'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def baixar_modelo(scale):
    model_path = f'RealESRGAN_x{scale}.pth'
    if not os.path.exists(model_path):
        url = f'https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5/RealESRGAN_x{scale}plus.pth'
        r = requests.get(url)
        with open(model_path, 'wb') as f:
            f.write(r.content)
    return model_path

@app.route('/', methods=['GET', 'POST'])
def index():
    enhanced_image = None

    if request.method == 'POST':
        file = request.files['image']
        scale = int(request.form.get('scale', 2))

        if file:
            filename = file.filename
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            img = Image.open(filepath).convert('RGB')

            model_path = baixar_modelo(scale)
            model = RealESRGAN(torch.device('cpu'), scale=scale)
            model.load_weights(model_path)

            enhanced = model.predict(img)
            enhanced_filename = f'enhanced_{filename}'
            enhanced_path = os.path.join(UPLOAD_FOLDER, enhanced_filename)
            enhanced.save(enhanced_path)

            enhanced_image = enhanced_filename

    with open('index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()

    return render_template_string(html_content, enhanced_image=enhanced_image)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
