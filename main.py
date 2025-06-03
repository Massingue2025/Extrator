from flask import Flask, render_template, request, send_from_directory
import os
import subprocess
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/outputs'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

RESOLUCOES = {
    "140p": "256:144",
    "240p": "426:240",
    "360p": "640:360",
    "480p": "854:480",
    "720p": "1280:720",
    "1080p": "1920:1080",
    "2k": "2560:1440",
    "4k": "3840:2160"
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        quality = request.form['quality']
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            output_filename = f"enhanced_{quality}_{filename}"
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)

            file.save(input_path)

            resolution = RESOLUCOES.get(quality, "1280:720")

            cmd = [
                'ffmpeg', '-y',
                '-i', input_path,
                '-vf', f"scale={resolution}",
                '-q:v', '2',
                output_path
            ]

            subprocess.run(cmd)

            return render_template('index.html', enhanced_image=output_filename)

    return render_template('index.html', enhanced_image=None)

@app.route('/static/outputs/<filename>')
def output_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

app.run(host='0.0.0.0', port=81)
