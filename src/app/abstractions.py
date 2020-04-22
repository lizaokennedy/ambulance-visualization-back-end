from flask import Flask
from app import app
from app.model import db, Simulation
from flask.json import jsonify
import json


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
        jsonSims.append({"Simulation": {"id": sims[i].id, "sim_start": sims[i].sim_start,
                                        "sim_end": sims[i].sim_end, "year": sims[i].year, "status": sims[i].status}})

    # print(json.dump(jsonSims))
    simulations = jsonify({"sims": jsonSims})
    return simulations
