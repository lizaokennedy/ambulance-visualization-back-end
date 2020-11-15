import operator
from flask.json import jsonify
from flask import request
from app import app
from app.postgresdb import *
from app.sumo import run, save_controller, Controller
from app.Optimize import *

@app.route("/")
def hello():
    return "Welcome to The Ambu-Lenz API"

@app.route("/api/getAllSimulations")
def getAllSimulations():
    sims = get_all_sims()
    return sims

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
    
    get_heatmap_points(simID)
    return get_avg_response_time(simID)

@app.route("/api/runSimulation")
def runSimulations():
    simID, success = run()
    print(simID, success)
    if (success):
        complete_simulation(simID)
    else: 
        remove_simulation(simID)
    return {'id': str(simID), 'success': success}

@app.route("/api/saveSettings", methods=['POST'])
def saveSettings():
    data = request.json
    print(data)
    c = Controller()
    c.parse_data(data)
    save_controller(c)
    data = 0
    return "Success"

@app.route("/api/getHeatmapPoints", methods=['POST'])
def getHeatmapPoints():
    data = request.json
    simID = data["simID"]
    return get_heatmap_points(simID)


@app.route("/api/removeSimulation", methods=['POST'])
def removeSimulation():
    data = request.json
    simID = data["simID"]
    return remove_simulation(simID)

@app.route("/api/removeOptimization", methods=['POST'])
def removeOptimization():
    data = request.json
    optID = data["optID"]
    return remove_optimization(optID)

@app.route("/api/runOptimization", methods=['POST'])
def optimize():
    data = request.json
    print(data)
    c = Controller(optimization=True)
    c.parse_data(data)
    save_controller(c)
    success = Optimize().run(c)
    if (not success):
        remove_simulation(simID)
    return {'success': success}
