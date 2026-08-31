import os
from flask import Flask, render_template, request, jsonify
import cloudinary
import cloudinary.uploader
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

# Cloudinary Configuration
cloudinary.config(
    cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME', 'pfmjg7ip'),
    api_key = os.environ.get('CLOUDINARY_API_KEY', '368463435529631'),
    api_secret = os.environ.get('CLOUDINARY_API_SECRET'),
    secure = True
)

def upload_single_file(file_data):
    index, file = file_data
    if file.filename != '':
        upload_result = cloudinary.uploader.upload(file, resource_type="auto")
        return {"order": index, "url": upload_result['secure_url']}
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'photos' not in request.files:
        return jsonify({'error': 'No files found'}), 400

    files = request.files.getlist('photos')
    files_with_index = list(enumerate(files))
    
    # Ek saath max 5 threads me fast upload hoga
    uploaded_results = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(upload_single_file, files_with_index)
        for res in results:
            if res:
                uploaded_results.append(res)
        
    uploaded_results.sort(key=lambda x: x['order'])
    final_urls = [item['url'] for item in uploaded_results]

    return jsonify({'urls': final_urls})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
    
