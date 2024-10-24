from flask import Flask, request, jsonify, send_file
from rembg import remove
from PIL import Image
import io
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        input_image = Image.open(file.stream)

        # Remove background using rembg
        output_image = remove(input_image)

        # Create a BytesIO object to store the image
        img_io = io.BytesIO()  # Instantiate BytesIO object
        output_image.save(img_io, format='PNG')
        img_io.seek(0)

        # Send the file back to the client as a PNG image
        return send_file(img_io, mimetype='image/png', download_name='removed-bg-image.png' ,as_attachment=True)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
