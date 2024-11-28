from datetime import datetime, timedelta
from app import db
from app.models import SensorLog
from sqlalchemy import func
from kafka import KafkaConsumer
from app.agents.occupancy_detector import OccupancyDetector
import json
import logging

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Initialize Kafka consumer
consumer = KafkaConsumer(
    'iot_data',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Initialize occupancy detector
occupancy_detector = OccupancyDetector()

def consume_iot_data():
    """Consume IoT data from Kafka and process it"""
    for message in consumer:
        data = message.value
        room_id = data['room_id']
        sensor_data = data['data']
        
        try:
            # Process occupancy
            occupancy_result = occupancy_detector.process_message({
                'room_id': room_id,
                'data': sensor_data,
                'timestamp': data['timestamp']
            })
            
            if occupancy_result:
                log_alert(room_id, f"Occupancy status: {occupancy_result['is_occupied']}")
            
            # Store in database
            sensor_log = SensorLog(
                room_id=room_id,
                sensor_type="aggregate",
                data=sensor_data
            )
            db.session.add(sensor_log)
            db.session.commit()
            
            logging.info(f"Processed data for room {room_id}")
            
        except Exception as e:
            logging.error(f"Error processing data for room {room_id}: {e}")

def log_alert(room_id, message):
    logging.info(f"{datetime.now()}: Alert in Room {room_id} - {message}")

def calculate_weekly_summary():
    """Your existing weekly summary code"""
    one_week_ago = datetime.now() - timedelta(days=7)
    
    results = db.session.query(
        SensorLog.room_id,
        func.avg(SensorLog.data['iaq']['co2'].cast(db.Float)).label('average_co2'),
        func.avg(SensorLog.data['iaq']['temperature'].cast(db.Float)).label('average_temperature')
    ).filter(SensorLog.timestamp >= one_week_ago) \
     .group_by(SensorLog.room_id) \
     .all()

    for result in results:
        print(f"Weekly Summary - Room {result.room_id}:")
        print(f"  Average CO2: {result.average_co2}")
        print(f"  Average Temperature: {result.average_temperature}")

if __name__ == "__main__":
    logging.info("Starting IoT data consumer...")
    consume_iot_data()
