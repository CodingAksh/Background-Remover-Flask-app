from flask import Flask, request, jsonify, send_file
from rembg import remove
from PIL import Image
import io
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    # Check if a file is included in the request
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    # Check if the file has a valid filename
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Open the image using PIL
        input_image = Image.open(file.stream)

        # Remove the background using rembg
        output_image = remove(input_image)

        # Save the output image to a BytesIO stream to avoid saving it on disk
        img_io = io.BytesIO
        output_image.save(img_io, format='PNG')
        img_io.seek(0)

        # Send the image file back to the client
        return send_file(img_io, mimetype='image/png', as_attachment=True)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
