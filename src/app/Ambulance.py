
class Ambulance:
    ambuID = 0
    src = 0
    dest = 0 
    emergencyID = 0
    depotID = 0
    returning = False
    
    def __init__(self, ambuID, src, dest, emergencyID, depotID):
        self.ambuID = ambuID
        self.src = src
        self.dest = dest
        self.emergencyID = emergencyID
        self.depotID = depotID
        self.returning = False

