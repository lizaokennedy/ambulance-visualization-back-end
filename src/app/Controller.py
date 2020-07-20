import traci
from app.Ambulance import Ambulance 
from app.Emergency import Emergency
from app.Depot import Depot

class Controller:
    depots = []
    emergencies = []
    ambulances = {}
    waiting = []
    emergencies_to_process = 0
    stop_time = 0


    def parse_data(self, data, randomGeneration=True, stop_time=2000):  
        data = self.get_dummy_data()
        self.stop_time = stop_time

        if not randomGeneration:
            counter = 0
            for e in data['emergency']:
                newEm = Emergency(counter, e["long"], e["lat"], e["time"])
                self.emergencies.append(newEm)
                counter += 1

            self.emergencies_to_process = counter + 1
            self.emergencies = sorted(self.emergencies, key=lambda x: x.time)

        counter = 0
        for h in data['hospital']: 
            newH = Depot(counter, h["long"], h["lat"], h["ambulances"])
            self.depots.append(newH)
            counter += 1

    def get_dummy_data(self):
        return {
            "emergency": [
            { "time": 13, "long": -33.814488, "lat": 18.479524 },
            { "time": 8, "long": -33.806133, "lat": 18.483682 },
            { "time": 43, "long": -33.791686, "lat": 18.504186 },
            { "time": 67, "long": -33.787819, "lat": 18.481804 },
            { "time": 97, "long": -33.804492, "lat": 18.487809 },
            { "time": 230, "long": -33.818350, "lat": 18.534776 },
            { "time": 450, "long": -33.804710, "lat": 18.525234 },
            { "time": 567, "long": -33.756806, "lat": 18.517333 },
            { "time": 789, "long": -33.777613, "lat": 18.449529 },
            { "time": 890, "long": -33.821400, "lat": 18.478422 },
            { "time": 1230, "long": -33.828479, "lat": 18.485627 },
            { "time": 1567, "long": -33.826066, "lat": 18.497805 },
            { "time": 1460, "long": -33.818170, "lat": 18.510749 },
            { "time": 17, "long": -33.817142, "lat": 18.514900 }
            ],
            "hospital": [
            { "long": -33.817307, "lat": 18.504812, "ambulances": 2 },
            { "long": -33.805127, "lat": 18.494672, "ambulances": 1 },
            { "long": -33.814518, "lat": 18.486162, "ambulances": 1 }
            ]
        }
