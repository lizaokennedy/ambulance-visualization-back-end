import traci
from app.Ambulance import Ambulance 
from app.Emergency import Emergency
from app.Depot import Depot
from app.postgresdb import create_heatpoint
import sumolib
import os


class Controller:

    def __init__(self, optimization=False):
        self.net = sumolib.net.readNet(os.path.abspath('app/data/blou.net.xml'))
        self.outData = []
        self.depots = []
        self.emergencies = []
        self.ambulances = {}
        self.waiting = 0
        self.emergencies_to_process = 0
        self.stop_time = 0
        self.prob = 0
        self.prob_static = 0
        self.simId = 0
        self.num_depots = 0
        self.num_ambulances = 0
        self.optimization = optimization

    def parse_data(self, data, randomGeneration=True):  
        counter = 0
        ambus = 0
        if self.optimization:
            ambus += int(data["ambulances"])
            for h in data['depots']: 
                newH = Depot(counter, h["coordinate"][1], h["coordinate"][0], 0)
                self.depots.append(newH)
                counter += 1
        else: 
            for h in data['depots']: 
                newH = Depot(counter, h["coordinate"][1], h["coordinate"][0], int(h["ambulances"]))
                ambus += int(h["ambulances"])
                self.depots.append(newH)
                counter += 1

        self.num_depots = counter
        self.num_ambulances = ambus
        self.stop_time = int(data['time'])
        self.prob = int(data['avgEmergencies'])/24/60/60
        self.prob_static = self.prob
        self.static_depots = self.depots


    def load_data(self, individual):
        for i in range(len(individual.position)): 
            self.depots[i].set_amubs(individual.position[i])
            
    def setID(self, simID):
        self.simId = simID

    def get_dummy_data(self):
        return {
            "emergency": [
            { "time": 13, "long": -33.814488, "lat": 18.479524 },
            { "time": 8, "long": -33.806133, "lat": 18.483682 },
            { "time": 17, "long": -33.817142, "lat": 18.514900 }
            ],
            'depots': [{'id': 2, 'coordinate': [18.486783337715565, -33.81526029503999], 'ambulances': '1'}],
            "time": 500,
            "avgEmergencies": 500
        }




