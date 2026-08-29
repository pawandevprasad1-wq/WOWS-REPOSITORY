import os
from flask import Flask, render_template, request, jsonify
import cloudinary
import cloudinary.uploader

app = Flask(__name__)

# Cloudinary Configuration
cloudinary.config(
    cloud_name="pfwjg7ip",
    api_key="368463435529631",
    api_secret="6u73nfIRo4ikkXSR_G021UT5tM",
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
                # resource_type="auto" aur chunk_size bada karke timeout error fix hota hai
                upload_result = cloudinary.uploader.upload(
                    file, 
                    resource_type="auto",
                    chunk_size=6000000  # 6MB chunks for smoother video upload
                )
                uploaded_urls.append(upload_result['secure_url'])

        return jsonify({"urls": uploaded_urls})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
    
