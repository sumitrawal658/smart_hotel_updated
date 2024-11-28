from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String, DateTime
from . import db
from datetime import datetime
from analytics import calculate_weekly_summary

Base = declarative_base()

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

class SensorLog(Base):
    __tablename__ = 'sensor_logs'
    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, nullable=False)
    sensor_type = Column(String(50), nullable=False)
    data = Column(db.JSON, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    synced = Column(db.Boolean, default=False)

class Device(db.Model):
    __tablename__ = 'devices'
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    device_type = db.Column(db.String(50), nullable=False)  # 'life_being' or 'iaq'
    status = db.Column(db.String(20), default='active')
    last_ping = db.Column(db.DateTime, default=datetime.utcnow)
    configuration = db.Column(db.JSON)