class Emergency:
    emID = 0
    long = 0
    lat = 0
    time = 0
    edge = 0
    x = 0
    y = 0


    def __init__(self, emID, long,lat, time):
        self.emID = emID
        self.long = long
        self.lat =lat
        self.time = time

    def set_edge(self, edge, x, y):
        self.edge = edge 
        self.x = x
        self.y = y

