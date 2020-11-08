from logging import error
import unittest
import sys
import os
from flask_cors import CORS
from app import app
sys.path.insert(0, 'src/app')
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from unittest import TestCase as Base

from app.postgresdb import create_simulation, remove_simulation, complete_simulation
from app.model import Simulation, Response, HeatPoint, db, setup
# from app import model

db = SQLAlchemy()

def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    return app


class MyConfig(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # app.config.from_pyfile('../dev_settings.py')

class TestCase(Base):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app(MyConfig())
        cls.client = cls.app.test_client()
        cls._ctx = cls.app.test_request_context()
        cls._ctx.push()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()   

    def setUp(self):
        self._ctx = self.app.test_request_context()
        self._ctx.push()
        db.session.begin(subtransactions=True)

    def tearDown(self):
        db.session.rollback()
        db.session.close()
        self._ctx.pop()


class TestModel(TestCase):

    def test_adding_simulation(self):
        sim = Simulation(0,0,0,0)
        db.session.add(sim)
        db.session.commit()
        assert sim in db.session

    def test_adding_heatpoint(self):
        hp = HeatPoint(0,0,0)
        db.session.add(hp)
        db.session.commit()
        id = hp.id
        assert hp in db.session

    def test_adding_response(self):
        r = Response(0,0,0,0,0,0)
        db.session.add(r)
        db.session.commit()
        assert r in db.session

    def test_pg_create_simulation(self):
        id = create_simulation(0,0,0,0)
        sim = Simulation.query.get(id)
        db.session.commit()
        assert sim.id == id

    def test_pg_remove_simulation(self):
        sim = Simulation(0,0,0,0)
        db.session.add(sim)
        db.session.commit()
        remove_simulation(sim.id)
        id = sim.id
        response = Simulation.query.filter(Simulation.id == id)
        assert "SELECT" in str(response)

    # def test_pg_complete_simulation(self):
    #     sim = Simulation(0,0,0,"0")
    #     db.session.add(sim)
    #     db.session.commit()
    #     id = sim.id + 1
    #     print("id: " ,id)
    #     complete_simulation(id)
    #     response = Simulation.query.filter(Simulation.id == id)
    #     # print(response.status)
    #     assert response.status == "Done"

if __name__ == "__main__":
    unittest.main()