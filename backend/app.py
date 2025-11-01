from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)
CORS(app)

client = MongoClient('mongodb://mongo:27017/')
db = client.devops_demo

@app.route('/api/health')
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/api/add', methods=['POST'])
def add_message():
    data = request.json
    result = db.messages.insert_one(data)
    # Convert ObjectId to string
    data['_id'] = str(result.inserted_id)
    return jsonify({"status": "success", "data": data}), 201

@app.route('/api/messages', methods=['GET'])
def get_messages():
    messages = list(db.messages.find({}, {'_id': 0}))
    return jsonify(messages), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)