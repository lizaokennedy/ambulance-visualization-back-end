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
from app.postgresdb import create_simulation, complete_simulation


def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true", default=False, help="run the commandline version of sumo")
    options, args = opt_parser.parse_args()
    return options

def run(randomGeneration=True):
    global step, c, activities
    activities = ""
    simId = create_simulation(0, c.stop_time, 2020, "Running")
    step = 0
    i = 0
    sumoBinary = checkBinary('sumo')
    traci.start([sumoBinary, "-c", "app/data/blou.sumocfg", "--tripinfo-output", "app/data/tripinfo.xml"])

    while (not stop()):
        traci.simulationStep()
        check_for_arrivals()

        if randomGeneration :
            if random() < c.prob:
                generate_emergency()
        else:
            i = process_emergency(i, step)
        step += 1

    complete_simulation(simId)
    traci.close()
    sys.stdout.flush()
    c = Controller
    step = 0
    return simId, activities

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
            print("\n" + str(c.emergencies_to_process) + " - INVALID (" + str(i) + ")")
            i += 1
        else:
            add_emergency(c.depots[depotID].edgeID, c.emergencies[i].edgeID, depotID)
            i += 1
    return i


def generate_emergency():
    global emergencyID, activities
    success = False
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
        print("\n" + str(c.emergencies_to_process) + " - Adding Successful!")
        emergencyID += 1
        return success
    else:
        # add to waiting list
        print("\nNone available")
        c.waiting += 1
        activities += "Emergency added to waiting - " + str(c.waiting) + "\n"
        return success

def get_edge_random():
    edges = traci.edge.getIDList()
    return choice(edges)

def stop(randomGeneration=True):
    if randomGeneration:
        # if c.stop_time <= traci.simulation.getTime() and c.emergencies_to_process <= 0:
        if c.stop_time <= traci.simulation.getTime():
            c.prob = 0
            if(c.emergencies_to_process <= 0):
                print(traci.simulation.getTime(), c.emergencies_to_process)
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
        print("ERROR")
        return False

    print("Emergency Added - Adding Ambulance:  " + str(emergencyID))
    add_ambulance(emergencyID, e1, e2, depotID)
    return True

def get_edge_geo(long, lat):
    global net
    radius = 1000
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
    print("\nNo close edges found")    
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
    for depot in available:
        dist = traci.simulation.getDistanceRoad(depot.edgeID, 0.1, emergency.edgeID, 0.1, isDriving=True)
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
    global c, emergencyID, activities
    pending = 0
    for key, ambu in c.ambulances.items():
        if (ambu.returning):
            pending = handle_arrival_depot(ambu)
        else:
            handle_arrival_emergency(ambu)

    for i in range(pending):
        activities += "Respond to waiting Emergency\n"
        if generate_emergency():
            c.waiting -= 1



def handle_arrival_depot(ambu):
    global activities
    arrived = traci.edge.getLastStepVehicleIDs(str(ambu.src))
    pending = 0
    if len(arrived) > 0:
        name = "ambulance" + str(ambu.ambuID)
        if name in arrived:
            depot = c.depots[ambu.depotID]
            c.emergencies_to_process -= 1
            activities += "Arrived at Depot: Ambulance:" + str(ambu.ambuID) + " at TimeStep: " + str(traci.simulation.getTime()) + "\n"
            if (c.waiting > 0):
                pending += 1

            depot.receive_ambulance()
            traci.vehicle.remove(name)
    return pending

def handle_arrival_emergency(ambu):
    global activities
    name = "ambulance" + str(ambu.ambuID)
    arrived = traci.edge.getLastStepVehicleIDs(str(ambu.dest))
    if len(arrived) > 0:
        name = "ambulance" + str(ambu.ambuID)
        if name in arrived:
            try:
                traci.vehicle.changeTarget(name, ambu.src)
                activities += "Arrived at Emergency: Ambulance:" + str(ambu.ambuID) + " at TimeStep: " + str(traci.simulation.getTime()) + "\n"
            except:
                #todo route to a nearby edge that will work? - apparently this happens when a route has already been defined...
                global net
                try:
                    edges = net.edge.getConnections(ambu.dest)
                    print(edges)
                    print("handle_arrival_emergency")
                    traci.vehicle.changeTarget(name, edges[0])
                except:
                    print(edges)
                    print("Broke Again")
                return
            ambu.returning = True

def sort_output():
    out = et.parse("app/data/tripinfo.xml")
    root = out.getroot()
    print(root[0])
            

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
c = Controller
activities = ""


