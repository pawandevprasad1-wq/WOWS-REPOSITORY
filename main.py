import os
from flask import Flask, render_template, request, jsonify
import cloudinary
import cloudinary.uploader

app = Flask(__name__)

# Cloudinary Configuration using Environment Variables
cloudinary.config(
    cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME', 'pfmjg7ip'),
    api_key = os.environ.get('CLOUDINARY_API_KEY', '368463435529631'),
    api_secret = os.environ.get('CLOUDINARY_API_SECRET'), # Render Environment Variable se lein
    secure = True
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'photos' not in request.files:
        return jsonify({'error': 'No files found'}), 400

    files = request.files.getlist('photos')
    uploaded_results = []

    try:
        for index, file in enumerate(files):
            if file.filename != '':
                upload_result = cloudinary.uploader.upload(
                    file, 
                    resource_type="auto"
                )
                uploaded_results.append({
                    "order": index,
                    "url": upload_result['secure_url']
                })
        
        uploaded_results.sort(key=lambda x: x['order'])
        final_urls = [item['url'] for item in uploaded_results]

        return jsonify({'urls': final_urls})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
    
