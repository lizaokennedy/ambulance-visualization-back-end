import traci
from sumolib import checkBinary
import sumolib
import os, json, sys, math, optparse
import traci.constants as tc
import traci.exceptions as ex
import xml.etree.ElementTree as et
from random import random, choice
from app.Controller import Controller
from app.Ambulance import Ambulance 
from app.Emergency import Emergency
from app.Depot import Depot
from app.postgresdb import create_simulation, create_heatpoint, get_avg_response_time, sort_output
# only check for arrivals if there are 
# add flag for when running optimization so dont add heatpoints to db
def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true", default=False, help="run the commandline version of sumo")
    options, args = opt_parser.parse_args()
    return options

def run(randomGeneration=True, individual=None, optimization=False):
    global step, c, activities
    activities = ""
    if not optimization:
        simId = create_simulation(0, c.stop_time, 2020, "Running")
    else:
        c.load_data(individual)
        simId = -1
    step = 0
    i = 0
    c.setID(simId)
    sumoBinary = checkBinary('sumo')
    
    try: 
        traci.start([sumoBinary, "-c", "app/data/blou.sumocfg", "--tripinfo-output", 
            "app/data/tripinfo.xml"])
        while (not stop()):
            traci.simulationStep()
            if c.emergencies_to_process > 0:
                check_for_arrivals()
            if (not optimization):
                get_positions()

            if randomGeneration :
                if random() < c.prob:
                    generate_emergency()
            else:
                i = process_emergency(i, step)
            step += 1
            
        traci.simulationStep()
        traci.close()
        sys.stdout.flush()
        step = 0
        sort_output(simId)
        
        if optimization:
            c.prob = c.prob_static
            return float(get_avg_response_time(simId))
        else:
            c = Controller() #reset controller
            print(activities)
            return simId, True
    except Exception as e:
        print(str(e))
        return simId, False

def save_controller(controller, randomGeneration=True):
    global c
    c = controller
    if (not randomGeneration):
        for em in c.emergencies:
            edge, x, y = get_edge_geo(em.long, em.lat)
            em.set_edge(edge.getID())
        
    for d in c.depots:
        edge, x, y = get_edge_geo(d.long, d.lat)
        d.set_edge(edge.getID())

# Used for when real data is parsed through
def process_emergency(i, step):
    global emergencyID
    while (i < len(c.emergencies) and step == c.emergencies[i].time):
        depotID, minDist = get_depot(c.emergencies[i])
        if minDist == -1:
            c.emergencies_to_process -= 1
            # print("\n" + str(c.emergencies_to_process) + " - INVALID (" + str(i) + ")")
            i += 1
        else:
            add_emergency(c.depots[depotID].edgeID, c.emergencies[i].edgeID, depotID)
            i += 1
    return i


def generate_emergency():
    global emergencyID, activities
    success = False
    try:
        if len(find_available_depot()) > 0:
            while not success: 
                minDist = -1
                while minDist == -1:
                    emergency_edgeID = get_edge_random()
                    e = Emergency(emergencyID)
                    e.set_edge(emergency_edgeID)
                    depotID, minDist = get_depot(e)
                    emergencyID += 1
                    if minDist == 0 and depotID == 0:
                        return 
                success = add_emergency(c.depots[depotID].edgeID, emergency_edgeID, depotID)
            c.emergencies_to_process += 1
            # print("\n" + str(c.emergencies_to_process) + " - Adding Successful!")
            emergencyID += 1
            return success
        else:
            # add to waiting list
            # print("\nNone available")
            c.waiting += 1
            # activities += "Emergency added to waiting - " + str(c.waiting) + "\n"
            return success
    except Exception as e:
        # print("Gen Emergency" , str(e))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return False

def get_edge_random():
    edges = traci.edge.getIDList()
    return choice(edges)

def stop(randomGeneration=True, optimization=True):
    if randomGeneration:
        # if c.stop_time <= traci.simulation.getTime() and c.emergencies_to_process <= 0:
        if c.stop_time <= traci.simulation.getTime():
            c.prob = 0
            if optimization:
                return True
            else:
                if(c.emergencies_to_process <= 0):
                    # print(traci.simulation.getTime(), c.emergencies_to_process)
                    return True
    else:
        if (c.emergencies_to_process <= 0):
            return True

    return False

def add_emergency(e1, e2, depotID):
    global emergencyID, c, activities
    if e1 == -1 or e2 == -1:
        return False

    emergencyID += 1
    try:
        traci.route.add("eResponse" + str(emergencyID), [e1, e2])
        traci.vehicle.add("ambulance" + str(emergencyID), "eResponse" + str(emergencyID), typeID="emergency")
        traci.vehicle.setStop("ambulance" + str(emergencyID), e2, duration=1, pos=0.1)
        activities += "Generated Ambulance:" + str(emergencyID) + " at TimeStep: " + str(traci.simulation.getTime()) + "\n"
    except (ex.TraCIException, ex.FatalTraCIError):
        traci.vehicle.remove("ambulance" + str(emergencyID))
        # print("ERROR: removing ambulance " + str(emergencyID))
        return False

    # print("Emergency Added - Adding Ambulance:  " + str(emergencyID))
    add_ambulance(emergencyID, e1, e2, depotID)
    return True

def get_edge_geo(long, lat):
    global net
    radius = 1000
    try:
        x, y = net.convertLonLat2XY(lat, long)
        edges = net.getNeighboringEdges(x,y, radius)
        if len(edges) > 0:
            minDist = edges[0][1]
            selectedEdge = edges[0][0]
            for edge, dist in edges:
                if dist < minDist:
                    minDist = dist
                    selectedEdge = edge
            return selectedEdge, x, y
        # print("\nNo close edges found")    
        return -1
    except Exception as e:
        # print("Get edge geo", str(e))
        return -1

def get_depot(emergency):
    global activities
    available = find_available_depot()
    depotID, minDist = find_closest(emergency, available)
    return depotID, minDist

def find_available_depot():
    available = []
    for depot in c.depots:
        if depot.ambulances > 0:
            available.append(depot)
    return available

def find_closest(emergency, available):
    minDist = float("inf")
    depotID = 0
    try:
        for depot in available:
            dist = traci.simulation.getDistanceRoad(depot.edgeID, 0.1, emergency.edgeID, 0.1, isDriving=True)
            if dist < minDist and dist > 0:
                minDist = dist 
                depotID = depot.depID

        if minDist == float("inf"):
            return -1, -1
        else:
            return depotID, minDist
    except Exception as e:
        print("@Find Closest - ", str(e))

def add_ambulance(ambuID, src, dest, depotID):
    a = Ambulance(ambuID, src, dest, depotID)
    c.depots[depotID].dispatch_ambulance()
    c.ambulances[a.ambuID] = a

def check_for_arrivals():

    global c, emergencyID, activities
    pending = []
    try:
        for key, ambu in c.ambulances.items():
            if (ambu.returning):
                ambuID = handle_arrival_depot(ambu)
                if ambuID != -1:
                    pending.append(ambuID)
            else:
                handle_arrival_emergency(ambu)

        for key in pending:
            ambu = c.ambulances.pop(key)
            if(c.waiting > 0):
                activities += "Respond to waiting Emergency\n"
                if generate_emergency():
                    c.waiting -= 1
    except Exception as e:
        print("@Check for arrivals - ", str(e))



def handle_arrival_depot(ambu):
    try:
        global activities
        arrived = traci.edge.getLastStepVehicleIDs(str(ambu.src))
        if len(arrived) > 0:
            name = "ambulance" + str(ambu.ambuID)
            if name in arrived:
                depot = c.depots[ambu.depotID]
                c.emergencies_to_process -= 1
                activities += "Arrived at Depot: Ambulance:" + str(ambu.ambuID) + " at TimeStep: " + str(traci.simulation.getTime()) + "\n"
                depot.receive_ambulance()
                # print("ambulance " + str(ambu.ambuID))
                traci.vehicle.remove(name)
                return ambu.ambuID
        return -1
    except Exception as e:
        print("@Arrival at depot - ", str(e))
        return -1

def handle_arrival_emergency(ambu):
    global activities
    edges = []
    try:
        name = "ambulance" + str(ambu.ambuID)
        arrived = traci.edge.getLastStepVehicleIDs(str(ambu.dest))
        if len(arrived) > 0:
            name = "ambulance" + str(ambu.ambuID)
            if name in arrived:
                try:
                    traci.vehicle.changeTarget(name, ambu.src)
                    activities += "Arrived at Emergency: Ambulance:" + str(ambu.ambuID) + " at TimeStep: " + str(traci.simulation.getTime()) + "\n"
                except Exception as e:
                    global net
                    # print("Failed", str(e))
                    try:
                        edges = net.edge.getConnections(ambu.dest)
                        # print(edges)
                        # print("handle_arrival_emergency")
                        traci.vehicle.changeTarget(name, edges[0])
                    except Exception as e:
                        print("Broke Again", str(e))
                    return
                ambu.returning = True
    except Exception as e:
        print("@Arrival at Emergency - ", str(e))

def get_positions():
    global net, activities
    for key, ambu in c.ambulances.items():
        name = "ambulance" + str(ambu.ambuID)
        try:
            pos = traci.vehicle.getPosition(name)
            if not (pos[0] == -1073741824.0 or pos[1] == -1073741824.0):
                lng, lat = net.convertXY2LonLat(pos[0], pos[1])
                create_heatpoint(lng, lat, c.simId)
                # self.outData.append({'position': [lng, lat], 'weight': 1 })
        except Exception as e:
            # print(str(e))
            depot = c.depots[ambu.depotID]
            c.emergencies_to_process -= 1
            activities += "Arrived at Depot: Ambulance:" + str(ambu.ambuID) + " at TimeStep: " + str(traci.simulation.getTime()) + "\n"
            depot.receive_ambulance()
            c.ambulances.pop(ambu.ambuID)
            return

if __name__ == '__main__':
    c = Controller()
    c.parse_data([])
    options = get_options()
    # check binary
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # # # traci starts sumo as a subprocess and then this script connects and runs
    # traci.start([sumoBinary, "-c", "app/data/blou.sumocfg",
    #              "--tripinfo-output", "app/data/tripinfo.xml"])
    run()

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

sumoBinary = os.path.join(os.environ['SUMO_HOME'], 'sumo')
sumoCmd = [sumoBinary, "-c", "data/blou.sumocfg"]
net = sumolib.net.readNet(os.path.abspath('app/data/blou.net.xml'))
step = 0
emergencyID = 0
c = Controller()
activities = ""


