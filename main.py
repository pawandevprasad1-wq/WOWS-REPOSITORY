import os
import base64
from flask import Flask, render_template, request, jsonify, session
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# Production mein ek secret key set karein
app.secret_key = os.environ.get("SECRET_KEY", "super_secret_golden_key_123")

# MongoDB Atlas URI (Render environment variable se aayega)
MONGO_URI = os.environ.get("MONGO_URI", "YOUR_MONGODB_ATLAS_CONNECTION_STRING")
client = MongoClient(MONGO_URI)
db = client['property_db']

users_col = db['users']
properties_col = db['properties']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name = data.get('name')
    password = data.get('password')

    if not name or not password:
        return jsonify({'success': False, 'message': 'Name aur Password dono zaruri hain!'}), 400

    if users_col.find_one({'name': name}):
        return jsonify({'success': False, 'message': 'Yeh Name pehle se registered hai!'}), 400

    hashed_password = generate_password_hash(password)
    users_col.insert_one({'name': name, 'password': hashed_password})
    return jsonify({'success': True, 'message': 'Account safalta-purvak ban gaya!'})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    name = data.get('name')
    password = data.get('password')

    user = users_col.find_one({'name': name})
    if user and check_password_hash(user['password'], password):
        session['user'] = name
        return jsonify({'success': True, 'message': 'Login safal raha!', 'user': name})
    
    return jsonify({'success': False, 'message': 'Galat Name ya Password!'}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return jsonify({'success': True})

@app.route('/api/post-property', methods=['POST'])
def post_property():
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Pehle login karein!'}), 401

    title = request.form.get('title')
    description = request.form.get('description')
    price = request.form.get('price')
    image_file = request.files.get('image')

    image_base64 = ""
    if image_file:
        # Photo ko Base64 format mein encode karke MongoDB mein JSON ki tarah save karein
        image_bytes = image_file.read()
        image_base64 = "data:" + image_file.content_type + ";base64," + base64.b64encode(image_bytes).decode('utf-8')

    property_data = {
        'posted_by': session['user'],
        'title': title,
        'description': description,
        'price': price,
        'image': image_base64
    }

    properties_col.insert_one(property_data)
    return jsonify({'success': True, 'message': 'Property successfully post ho gayi!'})

@app.route('/api/properties', methods=['GET'])
def get_properties():
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401

    props = list(properties_col.find({}, {'_id': 0}))
    return jsonify({'success': True, 'properties': props})

if __name__ == '__main__':
    app.run(debug=True)
    
