import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

CLOUDINARY_UPLOAD_URL = "https://api.cloudinary.com/v1_1/dcadlftsu/upload"
UPLOAD_PRESET = "mazenhamdi"

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    files = {'file': (file.filename, file.stream, file.mimetype)}

    response = requests.post(CLOUDINARY_UPLOAD_URL, files=files, data={'upload_preset': UPLOAD_PRESET})

    if response.status_code == 200:
        file_url = response.json().get("secure_url")
        return jsonify({"download_url": file_url})
    else:
        return jsonify({"error": "Failed to upload"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
