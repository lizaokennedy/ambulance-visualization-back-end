from flask import Flask
from flask_cors import CORS
from flask.json import jsonify

app = Flask(__name__)
cors = CORS(app)

@app.route("/api")
def home():
    return jsonify({'data': "Hello, Flask!"})