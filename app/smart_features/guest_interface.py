from flask import Blueprint, jsonify, request
from ..models import Room, Device, SensorLog, db
from datetime import datetime, timedelta
import asyncio

smart_bp = Blueprint('smart_features', __name__)

class SmartRoomController:
    def __init__(self, room_id):
        self.room_id = room_id
        
    def get_realtime_data(self):
        """Get latest sensor data for the room"""
        latest_log = SensorLog.query.filter_by(room_id=self.room_id)\
            .order_by(SensorLog.timestamp.desc()).first()
        if not latest_log:
            return None
        return latest_log.data
        
    def get_historical_data(self, hours=24):
        """Get historical sensor data"""
        start_time = datetime.utcnow() - timedelta(hours=hours)
        logs = SensorLog.query.filter(
            SensorLog.room_id == self.room_id,
            SensorLog.timestamp >= start_time
        ).order_by(SensorLog.timestamp.desc()).all()
        return [{'data': log.data, 'timestamp': log.timestamp} for log in logs]
        
    def control_device(self, device_type, command, parameters=None):
        """Control room devices"""
        device = Device.query.filter_by(
            room_id=self.room_id, 
            device_type=device_type
        ).first()
        
        if not device:
            return False, "Device not found"
            
        try:
            if device_type == "ac":
                return self._control_ac(command, parameters)
            elif device_type == "tv":
                return self._control_tv(command, parameters)
            elif device_type == "lights":
                return self._control_lights(command, parameters)
            else:
                return False, "Unsupported device type"
        except Exception as e:
            return False, str(e)
            
    def _control_ac(self, command, parameters):
        """Control air conditioner"""
        valid_commands = ['power', 'temperature', 'mode', 'fan_speed']
        if command not in valid_commands:
            return False, "Invalid AC command"
            
        # Update device configuration
        device = Device.query.filter_by(
            room_id=self.room_id, 
            device_type='ac'
        ).first()
        
        config = device.configuration or {}
        if command == 'power':
            config['power'] = parameters.get('state', 'off')
        elif command == 'temperature':
            config['temperature'] = parameters.get('value', 24)
        elif command == 'mode':
            config['mode'] = parameters.get('value', 'auto')
        elif command == 'fan_speed':
            config['fan_speed'] = parameters.get('value', 'auto')
            
        device.configuration = config
        db.session.commit()
        return True, "AC settings updated"

    def _control_tv(self, command, parameters):
        """Control television"""
        valid_commands = ['power', 'channel', 'volume']
        if command not in valid_commands:
            return False, "Invalid TV command"
            
        device = Device.query.filter_by(
            room_id=self.room_id, 
            device_type='tv'
        ).first()
        
        config = device.configuration or {}
        if command == 'power':
            config['power'] = parameters.get('state', 'off')
        elif command == 'channel':
            config['channel'] = parameters.get('number', 1)
        elif command == 'volume':
            config['volume'] = parameters.get('level', 50)
            
        device.configuration = config
        db.session.commit()
        return True, "TV settings updated" 