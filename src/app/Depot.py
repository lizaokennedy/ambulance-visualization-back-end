
class Depot:
    depID = 0
    long = 0
    lat = 0
    ambulances = 0
    edge = 0
    x = 0
    y = 0

    def __init__(self, depID, long, lat, ambulances):
        self.depID = depID
        self.long = long
        self.lat = lat
        self.ambulances = ambulances
    
    def set_edge(self, edge, x, y):
        self.edge = edge 
        self.x = x
        self.y = y

    def dispatch_ambulance(self):
        self.ambulances -= 1

    def receive_ambulance(self):
        self.ambulances += 1
