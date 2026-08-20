import os
from flask import Flask, render_template, request, jsonify
import cloudinary
import cloudinary.uploader

app = Flask(__name__)

# Direct Cloudinary Configuration
cloudinary.config(
    cloud_name="pfwjg7ip",
    api_key="368463435529631",
    api_secret="6u7lnfiRo4ikkXSR_G02iUt5tM",
    secure=True
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

    try:
        for file in files:
            if file.filename != '':
                upload_result = cloudinary.uploader.upload(file)
                uploaded_urls.append(upload_result['secure_url'])

        return jsonify({"urls": uploaded_urls})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
    
