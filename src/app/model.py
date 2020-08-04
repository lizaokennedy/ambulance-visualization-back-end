from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import *

db = SQLAlchemy()
migrate = Migrate()


def setup(app):
    db.init_app(app)
    migrate.init_app(app, db)


class Simulation(db.Model):
    __tablename__ = 'Simulation'

    id = db.Column('id', db.Integer, primary_key=True)
    sim_start = db.Column('Simulation_Start', db.Float, primary_key=False)
    sim_end = db.Column('Simulation_End', db.Float, primary_key=False)
    year = db.Column('Year', db.Integer, primary_key=False)
    status = db.Column('Status', db.Text, primary_key=False)

    def __init__(self, sim_start, sim_end, year, status):
        self.sim_start = sim_start
        self.sim_end = sim_end
        self.year = year
        self.status = status

    def __repr__(self, sim_start, sim_end, year, status):
        return f"<Simulation {self.status}>"

class HeatPoint(db.Model):
    __tablename__ = 'Heatpoint'

    id = db.Column('id', db.Integer, primary_key=True)
    lng = db.Column('longitude', db.Float, primary_key=False)
    lat = db.Column('latitude', db.Float, primary_key=False)
    version = db.Column('version', db.Integer, primary_key=False)

    def __init__(self, lng, lat, version):
        self.lng = lng
        self.lat = lat
        self.version = version

    def __repr__(self, lng, lat, version):
        return f"<HeatPoint {self.lng}, {self.lat}>"


class Response(db.Model):
    __tablename__ = 'Response'

    id = db.Column('id', db.Integer, primary_key=True)
    timeStart = db.Column('TimeStart', db.Float, primary_key=False)
    timeEnd = db.Column('TimeEnd', db.Float, primary_key=False)
    version = db.Column('Version', db.Integer, primary_key=False)
    duration = db.Column('Duration', db.Float, primary_key=False)
    length = db.Column('Length', db.Float, primary_key=False)


    def __init__(self, path, timeStart, timeEnd, duration, length, version):
        self.path = path
        self.timeStart = timeStart
        self.timeEnd = timeEnd
        self.version = version
        self.duration = duration
        self.length = length

    def __repr__(self, path, timeStart, timeEnd, duration, length, version):
        return f"<Response {self.timeStart}>"


class RoadSegment(db.Model):
    __tablename__ = 'RoadSegment'

    id = db.Column('id', db.Integer, primary_key=True)
    fromNode = db.Column('From', db.Integer, primary_key=False)
    toNode = db.Column('To', db.Float, primary_key=False)
    frequency = db.Column('Frequency', db.Float, primary_key=False)


    def __init__(self, fromNode, toNode, frequency):
        self.fromNode = fromNode
        self.toNode = toNode
        self.frequency = frequency

    def __repr__(self, fromNode, toNode, frequency):
        return f"<RoadSegment {self.fromNode} - {self.toNode}: {self.frequency}>"

