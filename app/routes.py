from flask import Blueprint, jsonify, request
from .models import Hotel, Floor, Room, SensorData
from .iot_simulator import simulate_sensor_data
from .models import SensorLog
from . import db
from .event_stream import event_stream
from redis import Redis
import json
from .cloud_db import CloudDatabaseManager
from .simulation_manager import SimulationManager
from .analytics import calculate_weekly_summary

# Create a blueprint for the routes
bp = Blueprint('main', __name__)

# Create a global simulation manager instance
sim_manager = SimulationManager()

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
    
    # Publish to event stream
    event_stream.publish_sensor_data(room_id, data)
    
    # Store in database
    sensor_log = SensorLog(
        room_id=room_id,
        sensor_type='combined',
        data=data
    )
    db.session.add(sensor_log)
    db.session.commit()
    
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

# Add a new endpoint to get stream data
@bp.route('/stream/latest', methods=['GET'])
def get_stream_data():
    count = request.args.get('count', default=10, type=int)
    events = event_stream.get_latest_events(count)
    return jsonify(events)

@bp.route('/rooms/<int:room_id>/occupancy', methods=['GET'])
def get_room_occupancy(room_id):
    redis_client = Redis(host='localhost', port=6379, db=0)
    
    # Get latest occupancy status from the occupancy stream
    latest = redis_client.xrevrange('occupancy_stream', count=1)
    
    if not latest:
        return jsonify({'error': 'No occupancy data available'}), 404
        
    occupancy_data = json.loads(latest[0][1][b'message'].decode())
    
    if occupancy_data['room_id'] != room_id:
        return jsonify({'error': 'No recent occupancy data for this room'}), 404
        
    return jsonify(occupancy_data)

@bp.route('/cloud/logs/<int:room_id>', methods=['GET'])
def get_cloud_logs(room_id):
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    cloud_db = CloudDatabaseManager()
    logs = cloud_db.get_cloud_data(
        room_id=room_id,
        start_date=start_date,
        end_date=end_date
    )
    
    return jsonify([{
        'room_id': log.room_id,
        'sensor_type': log.sensor_type,
        'data': log.data,
        'timestamp': log.timestamp
    } for log in logs])

@bp.route('/scale/deploy', methods=['POST'])
def deploy_scaled_simulation():
    data = request.get_json()
    hotels = data.get('hotels', 1)
    floors_per_hotel = data.get('floors_per_hotel', 1)
    rooms_per_floor = data.get('rooms_per_floor', 1)
    
    # Check resource requirements
    from .scaling_config import get_resource_requirements
    resources = get_resource_requirements(hotels, floors_per_hotel, rooms_per_floor)
    
    # Create the infrastructure
    try:
        for h in range(hotels):
            hotel = Hotel(name=f"Hotel_{h+1}")
            db.session.add(hotel)
            db.session.flush()
            
            for f in range(floors_per_hotel):
                floor = Floor(hotel_id=hotel.id, number=f+1)
                db.session.add(floor)
                db.session.flush()
                
                for r in range(rooms_per_floor):
                    room = Room(
                        floor_id=floor.id,
                        room_number=f"{f+1}{r+1:02d}"
                    )
                    db.session.add(room)
            
        db.session.commit()
        return jsonify({
            "status": "success",
            "message": "Scaled deployment created successfully",
            "resources": resources
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@bp.route('/simulate/hotel/<int:hotel_id>', methods=['POST', 'DELETE'])
def manage_hotel_simulation(hotel_id):
    """Start or stop simulation for an entire hotel"""
    if request.method == 'POST':
        rooms_count = sim_manager.start_simulation(hotel_id=hotel_id)
        return jsonify({
            'message': f'Started simulation for {rooms_count} rooms in hotel {hotel_id}'
        })
    else:
        rooms_stopped = sim_manager.stop_simulation(hotel_id=hotel_id)
        return jsonify({
            'message': f'Stopped simulation for {rooms_stopped} rooms in hotel {hotel_id}'
        })

@bp.route('/simulate/floor/<int:floor_id>', methods=['POST', 'DELETE'])
def manage_floor_simulation(floor_id):
    """Start or stop simulation for a floor"""
    if request.method == 'POST':
        rooms_count = sim_manager.start_simulation(floor_id=floor_id)
        return jsonify({
            'message': f'Started simulation for {rooms_count} rooms on floor {floor_id}'
        })
    else:
        rooms_stopped = sim_manager.stop_simulation(floor_id=floor_id)
        return jsonify({
            'message': f'Stopped simulation for {rooms_stopped} rooms on floor {floor_id}'
        })
