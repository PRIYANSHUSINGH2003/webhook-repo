from flask import Flask, request, jsonify, render_template
from flask_pymongo import PyMongo
from datetime import datetime
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# MongoDB configuration (default to localhost for development)
app.config["MONGO_URI"] = os.environ.get("MONGO_URI", "mongodb+srv://priyanshusingh:110044@cluster0.mjtyng5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
mongo = PyMongo(app)

def format_event(event):
    action = event.get('action')
    author = event.get('author')
    to_branch = event.get('to_branch')
    from_branch = event.get('from_branch')
    timestamp = event.get('timestamp')
    if action == 'PUSH':
        return f'"{author}" pushed to "{to_branch}" on {timestamp}'
    elif action == 'PULL_REQUEST':
        return f'"{author}" submitted a pull request from "{from_branch}" to "{to_branch}" on {timestamp}'
    elif action == 'MERGE':
        return f'"{author}" merged branch "{from_branch}" to "{to_branch}" on {timestamp}'
    return 'Unknown event'

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    # Add timestamp if not present
    if 'timestamp' not in data:
        data['timestamp'] = datetime.utcnow().strftime('%d %b %Y - %I:%M %p UTC')
    # Insert into MongoDB
    mongo.db.events.insert_one(data)
    return jsonify({'status': 'success'}), 201

@app.route('/events', methods=['GET'])
def get_events():
    # Return latest 20 events, newest first
    events = list(mongo.db.events.find().sort('timestamp', -1).limit(20))
    # Convert ObjectId to string and return structured data
    def event_to_dict(e):
        return {
            'id': str(e.get('_id', '')),
            'request_id': e.get('request_id', ''),
            'author': e.get('author', ''),
            'action': e.get('action', ''),
            'from_branch': e.get('from_branch', ''),
            'to_branch': e.get('to_branch', ''),
            'timestamp': e.get('timestamp', ''),
        }
    formatted = [event_to_dict(e) for e in events]
    return jsonify(formatted)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
