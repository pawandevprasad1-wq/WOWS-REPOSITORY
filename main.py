import os
from flask import Flask, render_template, request, jsonify
import cloudinary
import cloudinary.uploader

app = Flask(__name__)

# Cloudinary Configuration
cloudinary.config(
    cloud_name = 'pfmjg7ip',
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
    uploaded_results = []

    try:
        # Loop me index track karke upload karenge
        for index, file in enumerate(files):
            if file.filename != '':
                upload_result = cloudinary.uploader.upload(
                    file,
                    resource_type="auto"
                )
                # Serial order maintain karne ke liye index bhi save karenge
                uploaded_results.append({
                    "order": index,
                    "url": upload_result['secure_url']
                })

        # Files ko original choice/selection order me sort karein
        uploaded_results.sort(key=lambda x: x['order'])
        
        # Sorted URLs ki list return karein
        final_urls = [item['url'] for item in uploaded_results]

        return jsonify({"urls": final_urls})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
    
