from datetime import datetime
from ..models import db, SensorLog
from flask import current_app

class DataLoggerAgent:
    def __init__(self):
        self.app = current_app._get_current_object()

    def process_message(self, message):
        """Process and log sensor data to database"""
        with self.app.app_context():
            try:
                sensor_log = SensorLog(
                    room_id=message['room_id'],
                    sensor_type='combined',
                    data=message['data'],
                    timestamp=datetime.fromisoformat(message['timestamp'])
                )
                db.session.add(sensor_log)
                db.session.commit()
                return True
            except Exception as e:
                print(f"Error logging data: {e}")
                return False 