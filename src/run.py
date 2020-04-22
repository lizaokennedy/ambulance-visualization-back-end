
from flask_cors import CORS
from flask.json import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app import app

if __name__ == "__main__":
    app.run()

