from flask.json import jsonify
from flask import request
from app import app
from app.postgresdb import *
# from app.tigerdb import get_shortest_path, get_all_resources, get_num_responses,get_num_transfers, get_avg_response_time
from app.functions import get_reposnses_per_week
from app.sumo import run, save_controller, Controller

@app.route("/")
def hello():
    return "Welcome to The Ambu-Lenz API"

@app.route("/api/getAllSimulations")
def getAllSimulations():
    sims = get_all_sims()
    return sims

# @app.route("/api/getShortestPath")
# def getShortestPath():
#     startVertex = request.args.get('start')
#     endVertex = request.args.get('end')
#     max_depth = 2000
#     return get_shortest_path(startVertex, endVertex, max_depth)

# @app.route("/api/loadData")
# def loadData():
#     get_all_resources()
#     return 'Data Is Being Loaded Into Postgres'

# @app.route("/api/getResponseCalls")
# def responseCalls():
#     return get_reposnses_per_week()

@app.route("/api/getNumResponses",  methods=['POST'])
def getNumResponses():
    data = request.json
    simID = data["simID"]
    return get_total_responses(simID)

@app.route("/api/getAvgDistance",  methods=['POST'])
def getNumTransfers():
    data = request.json
    simID = data["simID"]
    return get_avg_distance(simID)

@app.route("/api/getAvgResponseTime", methods=['POST'])
def getAvgResponseTime():
    data = request.json
    simID = data["simID"]
    return get_avg_response_time(simID)

@app.route("/api/runSimulation")
def runSimulations():
    simID, activities = run()
    sort_output(simID)
    print(activities)
    return str(simID)

@app.route("/api/saveSettings", methods=['POST'])
def saveSettings():
    data = request.json
    print(data)
    c = Controller()
    c.parse_data(data)
    save_controller(c)
    data = 0
    return "Success"


