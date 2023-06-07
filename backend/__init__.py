# from werkzeug.security import generate_password_hash, check_password_hash
import json
from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
config_file = "config.json"
db = SQLAlchemy(app)


class Config:
    """Config class
    Contains main constants to generate metrics
    """
    def __init__(self, filename):
        with open(filename) as f:
            data = json.load(f)

        """Metrics settings"""
        self.purchase_price_min = data["metrics"]["purchase_price"]["min"]
        self.purchase_price_max = data["metrics"]["purchase_price"]["max"]

        self.pages_scrolled_min = data["metrics"]["pages_scrolled"]["min"]
        self.pages_scrolled_max = data["metrics"]["pages_scrolled"]["max"]

        self.call_success_min = data["metrics"]["call_success"]["min"]
        self.call_success_max = data["metrics"]["call_success"]["max"]

        """Modeling settings"""
        self.event_count_min = data["modeling"]["event_count"]["min"]
        self.event_count_max = data["modeling"]["event_count"]["max"]


config = Config(config_file)
