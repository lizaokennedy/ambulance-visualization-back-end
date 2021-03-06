from re import L
from flask import Flask
from sqlalchemy.sql.elements import True_
from app import app
from app.model import db, Simulation, Response, HeatPoint, Optimization, Depot
from flask.json import jsonify
import json
from sqlalchemy import func, and_
import xml.etree.ElementTree as et


def sort_output(simID):
    out = et.parse("app/data/tripinfo.xml")
    root = out.getroot()
    for child in root.findall('tripinfo'):
        if "ambulance" in child.attrib['id']:
            print(child.attrib['id'])
            create_response(child.attrib['depart'], child.attrib['arrival'], child.attrib['duration'], child.attrib['routeLength'], simID)


# def exists(fromNode, toNode):
#     exists = db.session.query(RoadSegment).filter(and_(RoadSegment.fromNode == fromNode, RoadSegment.toNode == toNode))
#     # length = db.session.query(RoadSegment).count()
#     occurences = exists.count()
#     if (occurences > 0):
#         return True
#     else:
#         return False
     
# def updateFrequency(fromNode, toNode):
#     segment = db.session.query(RoadSegment).filter(and_(RoadSegment.fromNode == fromNode, RoadSegment.toNode == toNode)).first()
#     segment.frequency += 1
#     db.session.commit()
#     return segment


def create_simulation(start, end, year, status):
    s = Simulation(sim_start=start, sim_end=end, year=year, status=status)
    db.session.add(s)
    db.session.commit()
    return s.id

def create_optimization():
    opt = Optimization(response_time=0, status="Running")
    db.session.add(opt)
    db.session.commit()
    return opt.id

def remove_optimization(ID):
    opt = Optimization.query.filter(Optimization.id == ID).delete()
    db.session.commit()

def complete_optimization(ID, response_time, depots):
    opt = Optimization.query.get(ID)
    opt.status = "Done"
    opt.response_time = response_time
    db.session.merge(opt)
    # add to db
    count = 1 
    for d in depots:
        d = Depot(localID=count, lng=d.long, lat=d.lat, ambulances=d.ambulances, version=ID)
        db.session.add(d)
        count += 1
    db.session.commit()

def remove_simulation(ID):
    sim = Simulation.query.filter(Simulation.id == ID).delete()
    db.session.commit()

def complete_simulation(simId):
    sim = Simulation.query.get(simId)
    sim.status = "Done"
    db.session.merge(sim)
    db.session.commit()

def create_response(timeStart, timeEnd, duration, length, version, path=0):
    r = Response(path, timeStart, timeEnd, duration, length, version)
    db.session.add(r)
    db.session.commit()
    return r.id

def create_heatpoint(lng,lat,version):
    h = HeatPoint(lng,lat,version)
    db.session.add(h)
    db.session.commit()
    return h.id

def get_all_sims():
    sims = db.session.query(Simulation)
    length = db.session.query(Simulation).count()
    jsonSims = []
    for i in range(length):
        jsonSims.append({"id": sims[i].id, "sim_start": sims[i].sim_start,
                                        "sim_end": sims[i].sim_end, "year": sims[i].year, "status": sims[i].status})

    simulations = jsonify({"sims": jsonSims})
    return simulations

def get_all_opts():
    opts = db.session.query(Optimization)
    length = db.session.query(Optimization).count()
    jsonOpts = []
    for i in range(length):
        jsonOpts.append({"id": opts[i].id, "status": opts[i].status, "response_time": opts[i].response_time})
        print(opts[i].response_time)
    optimizations = jsonify({"optimizations": jsonOpts})    
    return optimizations

def get_depots(optID):
    depots = db.session.query(Depot).filter(Depot.version == optID)
    jsonDepots = []
    for depot in depots:
        jsonDepots.append({"id": depot.localID, "lng": depot.lng, "lat": depot.lat, "ambulances": depot.ambulances})
    depots = jsonify({"depots": jsonDepots})    
    return depots

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

def get_opt_response_time(optID): 
    opt = db.session.query(Optimization).filter(Optimization.id == optID).first()
    return str(opt.response_time)

    
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

def get_total_responses(simId):
    total = db.session.query(Response).filter(Response.version == simId).count()
    return str(total)

def get_heatmap_points(simId):
    data = []
    points = db.session.query(HeatPoint).filter(HeatPoint.version == simId)
    for point in points:
        data.append([point.lng, point.lat])

    return {"points": data}
