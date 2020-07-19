import traci
from sumolib import checkBinary
import sumolib
import os, json, sys, math, optparse
import traci.constants as tc
from random import random, choice
from app.Controller import Controller
from app.Ambulance import Ambulance 
from app.Emergency import Emergency
from app.Depot import Depot


def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true", default=False, help="run the commandline version of sumo")
    options, args = opt_parser.parse_args()
    return options

def run():
    global step, c, prob
    step = 0
    i = 0
    sumoBinary = checkBinary('sumo')
    traci.start([sumoBinary, "-c", "app/data/blou.sumocfg", "--tripinfo-output", "app/data/tripinfo.xml"])

    while (not all_emergencies_processed() > 0 or traci.simulation.getMinExpectedNumber() > 0):
        traci.simulationStep()
        check_for_arrivals()
        i = process_emergency(i, step)
        step += 1

    traci.close()
    sys.stdout.flush()

def save_controller(controller):
    global c
    c = controller
    for em in c.emergencies:
        edge, x, y = get_edge(em.long, em.lat)
        em.set_edge(edge, x, y)
    
    for d in c.depots:
        edge, x, y = get_edge(d.long, d.lat)
        d.set_edge(edge, x, y)

def process_emergency(i, step):
    while (i < len(c.emergencies) and step == c.emergencies[i].time):
        depotID, minDist = get_depot(c.emergencies[i])
        if minDist == -1:
            c.emergencies_to_process -= 1
            print(str(c.emergencies_to_process) + " - INVALID (" + str(i) + ")")
            i += 1
        else:
            print("Adding Emergency #" + str(emergency) + " @ " + str(c.emergencies[i].time))
            add_emergency(c.depots[depotID].edge, c.emergencies[i].edge, depotID)
            i += 1
    return i

def all_emergencies_processed():
    if (c.emergencies_to_process > 0):
        return False
    else:
        return True

def add_emergency(e1, e2, depotID):
    global emergency, c
    if e1 == -1 or e2 == -1:
        return
    traci.route.add("eResponse" + str(emergency), [e1.getID(), e2.getID()])
    traci.vehicle.add("ambulance" + str(emergency), "eResponse" + str(emergency), typeID="emergency")
    try:
        traci.vehicle.setStop("ambulance" + str(emergency), e2.getID(), duration=1, pos=0.1)
    except:
        print("Could not add stop")

    add_ambulance(emergency, e1, e2, emergency, depotID)
    emergency += 1

def get_edge(long, lat):
    global net
    radius = 100
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
    print("No close edges found")    
    return -1

def get_depot(emergency):
    available = find_available_depot()
    if len(available) > 0:
        depotID, minDist = find_closest(emergency)
        return depotID, minDist
    else:
        print("None available")
        c.waiting.append(emergency)
        return -1, -1

def find_available_depot():
    available = []
    for depot in c.depots:
        if depot.ambulances > 0:
            available.append(depot)
    return available

def find_closest(emergency):
    minDist = float("inf")
    selectedEdge = c.depots[0].edge
    depotID = 0
    for depot in c.depots:
        dist = traci.simulation.getDistance2D(emergency.x, emergency.y, depot.x, depot.y,isDriving=True)
        if dist < minDist and dist > 0:
            minDist = dist 
            depotID = depot.depID
            selectedEdge = depot.edge

    if minDist == float("inf"):
        return -1, -1
    else:
        return depotID, minDist

def add_ambulance(ambuID, src, dest, emergencyID, depotID):
    a = Ambulance(ambuID, src, dest, emergencyID, depotID)
    c.depots[depotID].dispatch_ambulance()
    c.ambulances[a.ambuID] = a

def check_for_arrivals():
    for key, ambu in c.ambulances.items():
        if (ambu.returning):
            handle_arrival_depot(ambu)
        else:
            handle_arrival_emergency(ambu)

def handle_arrival_depot(ambu):
    arrived = traci.edge.getLastStepVehicleIDs(str(ambu.src.getID()))
    if len(arrived) > 0:
        name = "ambulance" + str(ambu.ambuID)
        if name in arrived:
            depot = c.depots[ambu.depotID]
            c.emergencies_to_process -= 1
            print(str(c.emergencies_to_process) + " - DEPOT (" + str(ambu.ambuID) + ")") 

            if len(c.waiting) > 0:
                emergency = c.waiting[0]
                dist = traci.simulation.getDistance2D(emergency.x, emergency.y, depot.x, depot.y,isDriving=True)
                if dist > 0:
                    depot.dispatch_ambulance()
                    add_emergency(depot.edge, emergency.edge, depot.depID)
                    c.waiting.pop(0)
            else:
                depot.receive_ambulance()
                traci.vehicle.remove(name)

def handle_arrival_emergency(ambu):
    name = "ambulance" + str(ambu.ambuID)
    traci.vehicle.getLaneID(name)
    arrived = traci.edge.getLastStepVehicleIDs(str(ambu.dest.getID()))
    if len(arrived) > 0:
        name = "ambulance" + str(ambu.ambuID)
        if name in arrived:
            traci.vehicle.changeTarget(name, ambu.src.getID())
            ambu.returning = True
            

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
emergency = 0
c = Controller
prob = 0.001


# def generate_emergency(i):
#     minDist = -1
#     while minDist == -1:
#         edgeID = find_location()
#         depotID, minDist = get_depot(c.emergencies[i])
    
#     print("Adding Emergency #" + str(emergency) + " @ " + str(traci.simulation.getTime()))
#     add_emergency(c.depots[depotID].edge.getID(), edgeID, depotID)
#     i += 1
#     return

# def find_location():
#     edges = traci.edges.getIDList()
#     return choice(edges)