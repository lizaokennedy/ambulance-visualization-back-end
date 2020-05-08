from flask import Flask
from app import app
from app.model import db, Simulation, RoadSegment
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


def get_all_sims():
    sims = db.session.query(Simulation).filter(Simulation.status == 'Done')
    length = db.session.query(Simulation).count()
    print(length)
    jsonSims = []
    for i in range(length):
        jsonSims.append({"id": sims[i].id, "sim_start": sims[i].sim_start,
                                        "sim_end": sims[i].sim_end, "year": sims[i].year, "status": sims[i].status})

    simulations = jsonify({"sims": jsonSims})
    return simulations
