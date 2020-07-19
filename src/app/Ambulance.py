
class Ambulance:
    ambuID = 0
    src = 0
    dest = 0 
    depotID = 0
    returning = False
    
    def __init__(self, ambuID, src, dest, depotID):
        self.ambuID = ambuID
        self.src = str(src)
        self.dest = str(dest)
        self.depotID = depotID
        self.returning = False

