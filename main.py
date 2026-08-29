import os
from flask import Flask, render_template, request, jsonify
import cloudinary
import cloudinary.uploader

app = Flask(__name__)

# Correct Cloudinary Credentials
cloudinary.config(
    cloud_name = 'pfmjp7ip',
    api_key = '368463435529631',
    api_secret = '6u7lnfIRo4ikkXSR_GM2ziUtStM',
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

    try:
        for file in files:
            if file.filename != '':
                # resource_type="auto" se photos aur videos dono upload hongi
                upload_result = cloudinary.uploader.upload(
                    file,
                    resource_type="auto"
                )
                uploaded_urls.append(upload_result['secure_url'])

        return jsonify({"urls": uploaded_urls})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
    
