from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import *
app = Flask(__name__)

app.config.from_pyfile('../dev_settings.py')
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:8080"]}})

from app.model import setup
from app import views
from app import model

setup(app)
