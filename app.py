from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image
from rembg import remove
import os

app = Flask(__name__)

# Configuration for file uploads
UPLOAD_FOLDER = 'static/uploads'
PROCESSED_FOLDER = 'static/processed'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

# Ensure upload and processed folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle image uploads
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        filenames = []
        for file in request.files.getlist('photo'):
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                filenames.append(filename)
        return redirect(url_for('process', filenames=','.join(filenames)))
    return redirect(url_for('index'))

# Route to process images and remove EXIF data
@app.route('/process/<filenames>', methods=['GET'])
def process(filenames):
    filenames = filenames.split(',')
    processed_filenames = []
    for filename in filenames:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image = Image.open(file_path)
        image_without_exif = remove_exif(image)
        processed_path = os.path.join(app.config['PROCESSED_FOLDER'], filename)
        image_without_exif.save(processed_path)
        processed_filenames.append(filename)
    return render_template('processed.html', filenames=processed_filenames)

def remove_exif(image):
    # Remove EXIF data from the image
    image_without_exif = image.copy()
    image_without_exif.info.clear()
    return image_without_exif

# Route to download processed images
@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['PROCESSED_FOLDER'], filename)

# Route to scan and process a folder
@app.route('/scan_folder', methods=['GET', 'POST'])
def scan_folder():
    if request.method == 'POST':
        folder_path = request.form['folder_path']
        filenames = [f for f in os.listdir(folder_path) if allowed_file(f)]
        processed_filenames = []
        for filename in filenames:
            file_path = os.path.join(folder_path, filename)
            image = Image.open(file_path)
            processed_image = remove(image)
            processed_path = os.path.join(app.config['PROCESSED_FOLDER'], filename)
            processed_image.save(processed_path)
            processed_filenames.append(filename)
        return render_template('processed.html', filenames=processed_filenames)
    return render_template('scan_folder.html')

if __name__ == '__main__':
    app.run(debug=True)
