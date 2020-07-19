class Emergency:
    emID = 0
    long = 0
    lat = 0
    time = 0
    edgeID = 0


    def __init__(self, emID, long=0 ,lat=0, time=0):
        self.emID = emID
        self.long = long
        self.lat =lat
        self.time = time

    def set_edge(self, edgeID):
        self.edgeID = str(edgeID)

