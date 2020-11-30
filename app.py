from flask import Flask, jsonify
import cmd_ui

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, flask!'

@app.route('/artists', methods=['GET'])
def get_artists():
    return jsonify({'artists': [a.name for a in cmd_ui.sorted_artists]})

app.run(port=5000)

