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
    
    get_heatmap_points(simID)
    return get_avg_response_time(simID)

@app.route("/api/runSimulation")
def runSimulations():
    simID, success = run()
    print(simID, success)
    if (success):
        complete_simulation(simID)
        sort_output(simID)
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

@app.route("/api/optimize")
def optimize():
    print("HIBICHECs")
    fitness, pos = Optimize.run(Optimize)
    return {'Fitness': fitness, 'Position': pos}
