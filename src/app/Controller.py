import traci
from app.Ambulance import Ambulance 
from app.Emergency import Emergency
from app.Depot import Depot

class Controller:

    def __init__(self):
        self.depots = []
        self.emergencies = []
        self.ambulances = {}
        self.waiting = 0
        self.emergencies_to_process = 0
        self.stop_time = 0
        self.prob = 0

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
