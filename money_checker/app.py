import os
from flask import Flask, request, render_template, flash
from werkzeug.utils import secure_filename
from processor import ImageProcessor
from extractor import FeatureExtractor
from predictor import NoteClassifier

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

class MoneyCheckerApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = 'replace-with-secure-key'
        self.app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        self.classifier = NoteClassifier()
        self.setup_routes()

    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def setup_routes(self):
        @self.app.route('/', methods=['GET', 'POST'])
        def index():
            if request.method == 'POST':
                if 'file' not in request.files:
                    flash('No file part')
                    return render_template('index.html')
                file = request.files['file']
                if file.filename == '':
                    flash('No selected file')
                    return render_template('index.html')
                if file and self.allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    path = os.path.join(self.app.config['UPLOAD_FOLDER'], filename)
                    os.makedirs(self.app.config['UPLOAD_FOLDER'], exist_ok=True)
                    file.save(path)

                    proc = ImageProcessor(path)
                    proc.load_image()
                    proc.to_grayscale()
                    proc.normalize()
                    roi = proc.extract_roi()

                    # Optional feature checks
                    feat = FeatureExtractor(roi)
                    wm = feat.watermark_detect('templates/watermark_template.jpg')
                    thread = feat.thread_detect()

                    label, prob = self.classifier.predict(roi)

                    return render_template('index.html', result=label, confidence=prob,
                                           watermark=wm, thread=thread)
            return render_template('index.html')

    def run(self, **kwargs):
        self.app.run(**kwargs)

if __name__ == '__main__':
    MoneyCheckerApp().run(host='0.0.0.0', port=5000, debug=True)