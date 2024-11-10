from . import db
from datetime import datetime

class Hotel(db.Model):
    __tablename__ = 'hotels'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

class Floor(db.Model):
    __tablename__ = 'floors'
    id = db.Column(db.Integer, primary_key=True)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotels.id'), nullable=False)
    number = db.Column(db.String(10), nullable=False)

class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    floor_id = db.Column(db.Integer, db.ForeignKey('floors.id'), nullable=False)
    room_number = db.Column(db.String(10), nullable=False)
    co2_threshold = db.Column(db.Float, default=800.0)
    temperature_threshold = db.Column(db.Float, default=25.0)

class SensorData(db.Model):
    __tablename__ = 'sensor_data'
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    sensor_type = db.Column(db.String(50))
    data = db.Column(db.JSON)   # Store sensor data as JSON
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

class SensorLog(db.Model):
    __tablename__ = 'sensor_logs'
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, nullable=False)
    sensor_type = db.Column(db.String(50), nullable=False)
    data = db.Column(db.JSON, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)