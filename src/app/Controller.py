import traci
from app.Ambulance import Ambulance 
from app.Emergency import Emergency
from app.Depot import Depot
from app.postgresdb import create_heatpoint
import sumolib
import os


class Controller:

    def __init__(self):
        self.net = sumolib.net.readNet(os.path.abspath('app/data/blou.net.xml'))
        self.outData = []
        self.depots = []
        self.emergencies = []
        self.ambulances = {}
        self.waiting = 0
        self.emergencies_to_process = 0
        self.stop_time = 0
        self.prob = 0
        self.simId = 0

    def parse_data(self, data, randomGeneration=True):  
        if not randomGeneration:
            counter = 0
            data = self.get_dummy_data()
            for e in data['emergency']:
                newEm = Emergency(counter, e["long"], e["lat"], e["time"])
                self.emergencies.append(newEm)
                counter += 1

            self.emergencies_to_process = counter + 1
            self.emergencies = sorted(self.emergencies, key=lambda x: x.time)

        counter = 0
        for h in data['depots']: 
            newH = Depot(counter, h["coordinate"][1], h["coordinate"][0], int(h["ambulances"]))
            self.depots.append(newH)
            counter += 1
        
        self.stop_time = int(data['time'])
        self.prob = int(data['avgEmergencies'])/24/60/60
        
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

    def get_positions(self):
        for key, ambu in self.ambulances.items():
            name = "ambulance" + str(ambu.ambuID)
            try:
                pos = traci.vehicle.getPosition(name)
                if not (pos[0] == -1073741824.0 or pos[1] == -1073741824.0):
                    lng, lat = self.net.convertXY2LonLat(pos[0], pos[1])
                    create_heatpoint(lng, lat, self.simId)
                    # self.outData.append({'position': [lng, lat], 'weight': 1 })
            except:
                return
            



