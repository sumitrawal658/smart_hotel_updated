from flask import Blueprint, jsonify, request
from .models import Hotel, Floor, Room, SensorData
from .iot_simulator import simulate_sensor_data
from .models import SensorLog
from . import db

# Create a blueprint for the routes
bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    return jsonify({"message": "Welcome to the Smart Hotel API!"})

@bp.route('/hotels', methods=['GET'])
def get_hotels():
    hotels = Hotel.query.all()
    return jsonify([{"id": hotel.id, "name": hotel.name} for hotel in hotels])

@bp.route('/hotels/<int:hotel_id>/floors', methods=['GET'])
def get_floors(hotel_id):
    floors = Floor.query.filter_by(hotel_id=hotel_id).all()
    return jsonify([{"id": floor.id, "number": floor.number} for floor in floors])

@bp.route('/floors/<int:floor_id>/rooms', methods=['GET'])
def get_rooms(floor_id):
    rooms = Room.query.filter_by(floor_id=floor_id).all()
    return jsonify([{"id": room.id, "room_number": room.room_number} for room in rooms])

@bp.route('/rooms/<int:room_id>/data', methods=['GET'])
def get_room_data(room_id):
    data = SensorData.query.filter_by(room_id=room_id).all()
    return jsonify([{"sensor_type": d.sensor_type, "data": d.data, "timestamp": d.timestamp} for d in data])

@bp.route('/simulate/<int:room_id>', methods=['POST'])
def simulate_room_data(room_id):
    data = simulate_sensor_data(room_id)
    return jsonify(data)

@bp.route('/simulate/<int:room_id>', methods=['GET'])
def get_simulated_data(room_id):
    """Endpoint to get simulated data for a room."""
    data = simulate_sensor_data(room_id)
    return jsonify(data)

# Endpoint to retrieve all sensor logs
@bp.route('/logs', methods=['GET'])
def get_all_logs():
    logs = SensorLog.query.all()
    return jsonify([{
        'id': log.id,
        'room_id': log.room_id,
        'sensor_type': log.sensor_type,
        'data': log.data,
        'timestamp': log.timestamp
    } for log in logs])

# Endpoint to retrieve logs for a specific room
@bp.route('/logs/<int:room_id>', methods=['GET'])
def get_logs_by_room(room_id):
    logs = SensorLog.query.filter_by(room_id=room_id).all()
    return jsonify([{
        'id': log.id,
        'sensor_type': log.sensor_type,
        'data': log.data,
        'timestamp': log.timestamp
    } for log in logs])

# Optional: Endpoint to log new sensor data manually
@bp.route('/logs', methods=['POST'])
def create_log():
    data = request.get_json()
    new_log = SensorLog(
        room_id=data['room_id'],
        sensor_type=data['sensor_type'],
        data=data['data']
    )
    db.session.add(new_log)
    db.session.commit()
    return jsonify({
        'message': 'New sensor log created.',
        'log': {
            'id': new_log.id,
            'room_id': new_log.room_id,
            'sensor_type': new_log.sensor_type,
            'data': new_log.data,
            'timestamp': new_log.timestamp
        }
    }), 201

@bp.route('/logs/<int:room_id>/recent', methods=['GET'])
def get_recent_logs(room_id):
    logs = SensorLog.query.filter_by(room_id=room_id).order_by(SensorLog.timestamp.desc()).limit(10).all()
    return jsonify([{
        'id': log.id,
        'sensor_type': log.sensor_type,
        'data': log.data,
        'timestamp': log.timestamp
    } for log in logs])

from sqlalchemy import func
from datetime import datetime

@bp.route('/logs/<int:room_id>/average', methods=['GET'])
def get_average_sensor_data(room_id):
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')

    if not start_time or not end_time:
        return jsonify({'error': 'Please provide both start_time and end_time parameters.'}), 400

    # Convert times from strings to datetime objects
    try:
        start_time = datetime.fromisoformat(start_time)
        end_time = datetime.fromisoformat(end_time)
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS).'}), 400

    # Example of calculating average CO2 and temperature for the given room and time range
    avg_co2 = db.session.query(func.avg(SensorLog.data['iaq']['co2'].cast(db.Float))) \
    .filter(SensorLog.room_id == room_id, SensorLog.timestamp >= start_time, SensorLog.timestamp <= end_time) \
    .scalar()

    avg_temperature = db.session.query(func.avg(SensorLog.data['iaq']['temperature'].cast(db.Float))) \
    .filter(SensorLog.room_id == room_id, SensorLog.timestamp >= start_time, SensorLog.timestamp <= end_time) \
    .scalar()


    return jsonify({
        'room_id': room_id,
        'average_co2': avg_co2,
        'average_temperature': avg_temperature
    })

@bp.route('/logs/<int:room_id>/latest', methods=['GET'])
def get_latest_sensor_status(room_id):
    latest_log = SensorLog.query.filter_by(room_id=room_id).order_by(SensorLog.timestamp.desc()).first()
    if not latest_log:
        return jsonify({'error': 'No logs found for the specified room.'}), 404

    return jsonify({
        'room_id': latest_log.room_id,
        'sensor_type': latest_log.sensor_type,
        'data': latest_log.data,
        'timestamp': latest_log.timestamp
    })

# routes.py

from flask import jsonify
from analytics import calculate_weekly_summary

@bp.route('/analytics/weekly_summary', methods=['GET'])
def get_weekly_summary():
    # Assuming `calculate_weekly_summary` returns a summary dictionary
    summary = calculate_weekly_summary()  # Modify if this function needs to interact with the database
    return jsonify(summary)

@bp.route('/rooms/<int:room_id>/thresholds', methods=['GET', 'PUT'])
def manage_thresholds(room_id):
    room = Room.query.get_or_404(room_id)
    if request.method == 'GET':
        return jsonify({
            "co2_threshold": room.co2_threshold,
            "temperature_threshold": room.temperature_threshold
        })
    elif request.method == 'PUT':
        data = request.json
        room.co2_threshold = data.get("co2_threshold", room.co2_threshold)
        room.temperature_threshold = data.get("temperature_threshold", room.temperature_threshold)
        db.session.commit()
        return jsonify({"message": "Thresholds updated successfully"})
