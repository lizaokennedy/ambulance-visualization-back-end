from flask import Flask
from app import app
from app.model import db, Simulation, RoadSegment, Response
from flask.json import jsonify
import json
from sqlalchemy import func, and_


def exists(fromNode, toNode):
    exists = db.session.query(RoadSegment).filter(and_(RoadSegment.fromNode == fromNode, RoadSegment.toNode == toNode))
    # length = db.session.query(RoadSegment).count()
    occurences = exists.count()
    if (occurences > 0):
        return True
    else:
        return False
     
def updateFrequency(fromNode, toNode):
    segment = db.session.query(RoadSegment).filter(and_(RoadSegment.fromNode == fromNode, RoadSegment.toNode == toNode)).first()
    segment.frequency += 1
    db.session.commit()
    return segment


def create_simulation(start, end, year, status):
    s = Simulation(sim_start=start, sim_end=end, year=year, status=status)
    db.session.add(s)
    db.session.commit()
    return s.id

def complete_simulation(simId):
    sim = Simulation.query.get(simId)
    sim.status = "Done"
    db.session.commit()

def create_response(timeStart, timeEnd, duration, length, version=0, path=0):
    r = Response(path, timeStart, timeEnd, duration, length, version)
    db.session.add(r)
    db.session.commit()

def get_all_sims():
    # s = Simulation(sim_start=0, sim_end=5000, year=2020, status="Done")
    # db.session.add(s)
    # db.session.commit()
    sims = db.session.query(Simulation)
    length = db.session.query(Simulation).count()
    print(length)
    jsonSims = []
    for i in range(length):
        print(i, length)
        jsonSims.append({"id": sims[i].id, "sim_start": sims[i].sim_start,
                                        "sim_end": sims[i].sim_end, "year": sims[i].year, "status": sims[i].status})

    simulations = jsonify({"sims": jsonSims})
    return simulations

