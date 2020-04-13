from flask_cors import CORS
from flask.json import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:docker@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

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


if __name__ == "__main__":
    app.run()
