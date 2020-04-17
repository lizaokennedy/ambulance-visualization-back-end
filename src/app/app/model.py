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


class Path(db.Model):
    __tablename__ = 'Path'

    id = db.Column('id', db.Integer, primary_key=True)
    path = db.Column('Path', db.ARRAY(db.Integer, dimensions=2), primary_key=False)  

    def __init__(self, path):
        self.path = path

    def __repr__(self, path):
        return f"<Path {self.status}>"


class Response(db.Model):
    __tablename__ = 'Response'

    id = db.Column('id', db.Integer, primary_key=True)
    path = db.Column('Simulation_Start', db.Integer, primary_key=False)  
    timeStart = db.Column('Simulation_End', db.Float, primary_key=False)    
    timeEnd = db.Column('Year', db.Float, primary_key=False)
    version = db.Column('Status', db.Integer, primary_key=False)


    def __init__(self, path, timeStart, timeEnd, version):
        self.path = path
        self.timeStart = timeStart
        self.timeEnd = timeEnd
        self.version = version

    def __repr__(self, sim_start, sim_end, year, status):
        return f"<Response {self.status}>"



from app import views