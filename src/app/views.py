from flask.json import jsonify
from app import app
from app.abstractions import create_simulation, get_all_sims


@app.route("/api")
def testAPI():
    return 'This is the home page'


@app.route("/api/getAllSimulations")
def getAllSimulations():
    sims = get_all_sims()
    return sims
