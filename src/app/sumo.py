import traci
from sumolib import checkBinary
import sumolib
import os, json, sys, math, optparse
import traci.constants as tc
import traci.exceptions as ex
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

def run(randomGeneration=True):
    global step, c, prob
    step = 0
    i = 0
    sumoBinary = checkBinary('sumo')
    traci.start([sumoBinary, "-c", "app/data/blou.sumocfg", "--tripinfo-output", "app/data/tripinfo.xml"])

    while (not stop() or traci.simulation.getMinExpectedNumber() > 0):
        traci.simulationStep()
        check_for_arrivals()
        if randomGeneration :
            if random() < prob:
                i = generate_emergency(i)
        else:
            i = process_emergency(i, step)
        step += 1

    traci.close()
    sys.stdout.flush()

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

def process_emergency(i, step):
    while (i < len(c.emergencies) and step == c.emergencies[i].time):
        depotID, minDist = get_depot(c.emergencies[i])
        if minDist == -1:
            c.emergencies_to_process -= 1
            print(str(c.emergencies_to_process) + " - INVALID (" + str(i) + ")")
            i += 1
        else:
            print("Adding Emergency #" + str(emergency) + " @ " + str(c.emergencies[i].time))
            add_emergency(c.depots[depotID].edgeID, c.emergencies[i].edgeID, depotID)
            i += 1
    return i


def generate_emergency(i):
    global emergency
    success = False
    while not success: 
        minDist = -1
        while minDist == -1:
            emergency_edgeID = get_edge_random()
            e = Emergency(emergency)
            e.set_edge(emergency_edgeID)
            depotID, minDist = get_depot(e)
        
        success = add_emergency(c.depots[depotID].edgeID, emergency_edgeID, depotID)
    c.emergencies_to_process += 1
    print(str(c.emergencies_to_process) + " - Added")
    # print("Added Emergency #" + str(emergency) + " @ " + str(traci.simulation.getTime()))
    i += 1
    return i

def get_edge_random():
    edges = traci.edge.getIDList()
    return choice(edges)

def stop(randomGeneration=True):
    global prob
    if randomGeneration:
        # if c.stop_time <= traci.simulation.getTime() and c.emergencies_to_process <= 0:
        if c.stop_time <= traci.simulation.getTime():
            prob = 0
            if(c.emergencies_to_process <= 0):
                return True
    else:
        if (c.emergencies_to_process <= 0):
            return True

    return False

def add_emergency(e1, e2, depotID):
    global emergency, c
    if e1 == -1 or e2 == -1:
        return False

    emergency += 1
    try:
        traci.route.add("eResponse" + str(emergency), [e1, e2])
        traci.vehicle.add("ambulance" + str(emergency), "eResponse" + str(emergency), typeID="emergency")
        traci.vehicle.setStop("ambulance" + str(emergency), e2, duration=1, pos=0.1)
        print("SUCCESS")
    except (ex.TraCIException, ex.FatalTraCIError):
        traci.vehicle.remove("ambulance" + str(emergency))
        print("ERROR")
        return False

    print("Adding " + str(emergency))
    add_ambulance(emergency, e1, e2, depotID)
    return True

def get_edge_geo(long, lat):
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
    depotID = 0
    for depot in c.depots:
        dist = traci.simulation.getDistanceRoad(depot.edgeID, 0.1, emergency.edgeID, 0.1, isDriving=True)
        # dist = traci.simulation.getDistance2D(emergency.x, emergency.y, depot.x, depot.y,isDriving=True)
        if dist < minDist and dist > 0:
            minDist = dist 
            depotID = depot.depID

    if minDist == float("inf"):
        return -1, -1
    else:
        return depotID, minDist

def add_ambulance(ambuID, src, dest, depotID):
    a = Ambulance(ambuID, src, dest, depotID)
    c.depots[depotID].dispatch_ambulance()
    c.ambulances[a.ambuID] = a

def check_for_arrivals():
    for key, ambu in c.ambulances.items():
        if (ambu.returning):
            handle_arrival_depot(ambu)
        else:
            handle_arrival_emergency(ambu)

def handle_arrival_depot(ambu):
    arrived = traci.edge.getLastStepVehicleIDs(str(ambu.src))
    if len(arrived) > 0:
        name = "ambulance" + str(ambu.ambuID)
        if name in arrived:
            depot = c.depots[ambu.depotID]
            c.emergencies_to_process -= 1
            print(str(c.emergencies_to_process) + " - DEPOT (" + str(ambu.ambuID) + ")") 

            if len(c.waiting) > 0:
                emergency = c.waiting[0]
                dist = traci.simulation.getDistanceRoad(emergency.edgeID, depot.edgeID)
                # dist = traci.simulation.getDistance2D(emergency.x, emergency.y, depot.x, depot.y,isDriving=True)
                if dist > 0:
                    depot.dispatch_ambulance()
                    add_emergency(depot.edgeID, emergency.edgeID, depot.depID)
                    c.waiting.pop(0)
            else:
                depot.receive_ambulance()
                traci.vehicle.remove(name)

def handle_arrival_emergency(ambu):
    name = "ambulance" + str(ambu.ambuID)
    arrived = traci.edge.getLastStepVehicleIDs(str(ambu.dest))
    if len(arrived) > 0:
        name = "ambulance" + str(ambu.ambuID)
        if name in arrived:
            try:
                traci.vehicle.changeTarget(name, ambu.src)
            except:
                #?route to a nearby edge that will work?
                print("handle_arrival_emergency")
                return
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
prob = 0.0009

