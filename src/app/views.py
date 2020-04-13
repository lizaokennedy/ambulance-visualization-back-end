from flask.json import jsonify
from app import app

@app.route("/api")
def home():
    return jsonify({'data': 'This is the home page'})