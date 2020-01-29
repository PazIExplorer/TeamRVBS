# Flask config
from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

# SQL Config
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Routes config
from app import routes, models