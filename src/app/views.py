from flask.json import jsonify
from flask import request
from app import app
from app.abstractions import create_simulation, get_all_sims
from app.tigerdb import get_shortest_path


@app.route("/api")
def testAPI():
    return 'This is the home page'


@app.route("/api/getAllSimulations")
def getAllSimulations():
    sims = get_all_sims()
    return sims


@app.route("/api/getShortestPath")
def getShortestPath():
    startVertex = request.args.get('start')
    endVertex = request.args.get('end')
    max_depth = 2000
    return get_shortest_path(startVertex, endVertex, max_depth)
