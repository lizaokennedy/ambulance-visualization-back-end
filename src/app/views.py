from flask.json import jsonify
from flask import request
from app import app
from app.postgresdb import create_simulation, get_all_sims, updateFrequency
from app.tigerdb import get_shortest_path, get_all_resources,getAllResponseCallTimes
from app.functions import get_reposnses_per_week

@app.route("/")
def hello():
    return "Welcome to The Ambu-Lenz API"

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
def loadData():
    get_all_resources()
    return 'Data Is Being Loaded Into Postgres'

@app.route("/api/getResponseCalls")
def responseCalls():
    return get_reposnses_per_week()
