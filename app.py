
from flask import Flask, request, render_template, send_file
from rembg import remove
from PIL import Image
import io
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part"
        file = request.files['file']
        if file.filename == '':
            return "No selected file"

        if file:
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)

            try:
                input_image = Image.open(filename)
                output_image = remove(input_image)

                img_io = io.BytesIO()
                output_image.save(img_io, 'PNG')
                img_io.seek(0)

                os.remove(filename)

                return send_file(img_io, mimetype='image/png', as_attachment=True, download_name='image_no_bg.png')
            except Exception as e:
                return f"Error processing image: {e}"

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
