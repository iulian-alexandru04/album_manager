from flask import Flask, jsonify, request
from main import Artist
import cmd_ui

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, flask!'

@app.route('/artist', methods=['POST'])
def add_artist():
    request_data = request.get_json()
    artist = Artist(request_data['name'], request_data['country'])
    cmd_ui.sorted_artists.append(artist)
    return jsonify({})

@app.route('/artists', methods=['GET'])
def get_artists():
    return jsonify({'artists': [a.name for a in cmd_ui.sorted_artists]})

app.run(port=5000)

