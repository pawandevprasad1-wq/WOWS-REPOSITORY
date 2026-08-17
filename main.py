import os
from flask import Flask, render_template, request, jsonify
import cloudinary
import cloudinary.uploader

app = Flask(__name__)

# Render Environment Variables se credentials automatic read hongi
cloudinary.config(
    cloud_name = os.environ.get("CLOUDINARY_CLOUD_NAME"),
    api_key = os.environ.get("CLOUDINARY_API_KEY"),
    api_secret = os.environ.get("CLOUDINARY_API_SECRET"),
    secure = True
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'photos' not in request.files:
        return jsonify({"error": "No files found"}), 400
    
    files = request.files.getlist('photos')
    uploaded_urls = []

    for file in files:
        if file.filename != '':
            upload_result = cloudinary.uploader.upload(file)
            uploaded_urls.append(upload_result['secure_url'])

    return jsonify({"urls": uploaded_urls})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
