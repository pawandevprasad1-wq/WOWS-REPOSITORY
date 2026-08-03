import os
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

MONGO_URI = "mongodb+srv://pawandevprasad1_db_user:123451234500@cluster0.acobnxp.mongodb.net/?appName=Cluster0"
DB_NAME = "WOW"
COLLECTION_NAME = "WOW"

try:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    client.admin.command('ping')
    print("Connected to MongoDB successfully!")
except Exception as e:
    print(f"MongoDB Connection Error: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify([])
    
    regex_query = {"$regex": query, "$options": "i"}
    db_filter = {
        "$or": [
            {"name": regex_query},
            {"location": regex_query},
            {"phone no.": regex_query},
            {"id": regex_query}
        ]
    }
    
    try:
        results = list(collection.find(db_filter, {"_id": 0}))
        return jsonify(results)
    except Exception as e:
        print(f"Search error: {e}")
        return jsonify([])

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
    
