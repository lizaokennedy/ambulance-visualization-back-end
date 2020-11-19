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


class Optimization(db.Model):
    __tablename__ = 'Optimization'

    id = db.Column('id', db.Integer, primary_key=True)
    status = db.Column('Status', db.Text, primary_key=False)
    response_time = db.Column('Response_time', db.Float, primary_key=False)

    def __init__(self, status, response_time):
        self.status = status
        self.response_time = response_time

    def __repr__(self, status, response_time,):
        return f"<Optimization {self.status} - {self.response_time}>"


class Depot(db.Model):
    __tablename__ = 'Depot'

    id = db.Column('id', db.Integer, primary_key=True)
    localID = db.Column('localID', db.Integer, primary_key=False)
    lng = db.Column('lng', db.Float, primary_key=False)
    lat = db.Column('lat', db.Float, primary_key=False)
    ambulances = db.Column('ambulances', db.Float, primary_key=False)
    version = db.Column('version', db.Integer, primary_key=False)

    def __init__(self, localID, lng, lat, ambulances, version):
        self.localID = localID
        self.lng = lng
        self.lat = lat
        self.ambulances = ambulances
        self.version = version

    def __repr__(self, lng, lat, ambulances, version):
        return f"<Depot {self.lng}, {self.lat}. {self.ambulances}>"
