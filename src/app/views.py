from flask.json import jsonify
from flask import request
from app import app
from app.abstractions import create_simulation, get_all_sims, updateFrequency
from app.tigerdb import get_shortest_path, get_all_resources

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

@app.route("/api/loadData")
def testAPI():
    # get_all_resources()
    # get_shortest_path(1,5,10)
    return 'This is the home page'