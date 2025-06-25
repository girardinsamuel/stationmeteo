from datetime import datetime
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from typing import List
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, func
import random
from sqlalchemy import cast, Date
from datetime import date as date_func, datetime


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class Sensor(db.Model):
    __tablename__ = "sensors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    logs = db.relationship("Log", back_populates="sensor")
    simple = db.Column(db.Boolean)


class Log(db.Model):
    __tablename__ = "logs"
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    temperature = db.Column(db.Float)
    pressure = db.Column(db.Float)
    humidity = db.Column(db.Float)
    rain = db.Column(db.Float)
    light = db.Column(db.Float)
    wind_speed = db.Column(db.Float)
    battery = db.Column(db.Float)
    battery_level = db.Column(db.Integer)
    sensor_id = db.Column(db.Integer, db.ForeignKey("sensors.id"))
    sensor = db.relationship("Sensor", back_populates="logs")


app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///weather_db.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# initialize the app with the extension
db.init_app(app)


@app.template_filter()
def date(value, format="datetime"):
    if isinstance(value, str) or not value:
        return value
    if format == "datetime":
        format = "%d/%m/%y à %H:%M:%S"
    elif format == "time":
        format = "%H:%M:%S"
    return value.strftime(format)


@app.route("/")
def home():
    """Show last measurement of all sensors."""

    sensors = Sensor.query.all()
    for sensor in sensors:
        sensor.last_log = sensor.logs[-1] if sensor.logs else None

    return render_template("home.html", sensors=sensors)


@app.route("/modules/<sensor_id>")
def sensor_detail(sensor_id):
    """Show measurement of the current day."""
    # sensor = {
    #     "name": "Maison",
    #     "id": sensor_id,
    #     "data": {"temperature": 20, "humidity": 50},
    # }
    sensor = Sensor.query.get_or_404(sensor_id)

    sensor.last_log = sensor.logs[-1] if sensor.logs else None

    today = datetime.today().date()

    logs = (
        Log.query.filter(Log.sensor_id == sensor.id)
        .filter(func.date(Log.timestamp) == today)
        .all()
    )
    return render_template("sensor.html", sensor=sensor, logs=logs)


@app.route("/modules/<sensor_id>/log")
def sensor_log(sensor_id):
    """View for testing only."""
    # sensor = {
    #     "name": "Maison",
    #     "id": sensor_id,
    #     "data": {"temperature": 20, "humidity": 50},
    # }

    log = Log(
        sensor_id=sensor_id,
        timestamp=datetime.now(),
        temperature=random.randint(10, 25),
        humidity=random.randint(40, 65),
    )
    db.session.add(log)
    db.session.commit()

    return f"Logged to {sensor_id}"
