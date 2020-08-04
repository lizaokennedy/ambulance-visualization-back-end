from flask import Flask
from app import app
from app.model import db, Simulation, RoadSegment, Response, HeatPoint
from flask.json import jsonify
import json
from sqlalchemy import func, and_
import xml.etree.ElementTree as et


def sort_output(simID):
    out = et.parse("app/data/tripinfo.xml")
    root = out.getroot()
    for child in root.findall('tripinfo'):
        if "ambulance" in child.attrib['id']:
            create_response(child.attrib['depart'], child.attrib['arrival'], child.attrib['duration'], child.attrib['routeLength'], simID)
            # print(child.attrib['depart'])


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

def remove_simulation(ID):
    sim = db.session.query(Simulation).filter(Simulation.id == ID)
    db.session.delete(sim)
    db.session.commit()
    print("deleted", ID)

def complete_simulation(simId):
    sim = Simulation.query.get(simId)
    sim.status = "Done"
    db.session.commit()

def create_response(timeStart, timeEnd, duration, length, version, path=0):
    r = Response(path, timeStart, timeEnd, duration, length, version)
    db.session.add(r)
    db.session.commit()

def create_heatpoint(lng,lat,version):
    h = HeatPoint(lng,lat,version)
    db.session.add(h)
    db.session.commit()

def get_all_sims():
    sims = db.session.query(Simulation)
    length = db.session.query(Simulation).count()
    jsonSims = []
    for i in range(length):
        jsonSims.append({"id": sims[i].id, "sim_start": sims[i].sim_start,
                                        "sim_end": sims[i].sim_end, "year": sims[i].year, "status": sims[i].status})

    simulations = jsonify({"sims": jsonSims})
    return simulations

def get_avg_response_time(simId=26):
    responses = db.session.query(Response).filter(Response.version == simId)
    total = 0
    count = 0
    for r in responses:
        total += r.duration/2
        count += 1
    if total == 0 :
        return str(0)
    else:
        return str(total/count/60)

    
def get_avg_distance(simId=26):
    responses = db.session.query(Response).filter(Response.version == simId)
    total = 0
    count = 0
    for r in responses:
        total += r.length/2
        count += 1
    if total == 0 :
        return str(0)
    else:
        return str(total/count/1000)

def get_total_responses(simId=26):
    total = db.session.query(Response).filter(Response.version == simId).count()
    return str(total)

