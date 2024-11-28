from app import create_app, db
from app.models import SensorLog
from kafka import KafkaProducer
import time
import requests
import logging
import json

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

app = create_app()
app.app_context().push()

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def fetch_and_log_data(room_id, interval=5):
    """Fetch data from the IoT simulation endpoint and publish to Kafka"""
    url = f'http://127.0.0.1:5000/simulate/{room_id}'
    while True:
        try:
            response = requests.get(url)
            data = response.json()
            
            # Check presence state to adjust sensor data
            if data['life_being']['presence_state'] == 'absent':
                data['iaq']['temperature'] = 18
                data['iaq']['illuminance'] = 50
                data['iaq']['noise'] = 20
                data['iaq']['humidity'] = 35.0

            # Publish to Kafka
            producer.send('iot_data', {
                'room_id': room_id,
                'data': data,
                'timestamp': time.time()
            })

            # Log to database
            new_log = SensorLog(
                room_id=room_id,
                sensor_type="aggregate",
                data=data
            )
            db.session.add(new_log)
            db.session.commit()
            
            logging.info(f"Data for room {room_id} sent to Kafka: {data}")
        except Exception as e:
            logging.error(f"Error fetching/publishing data for room {room_id}: {e}")
        time.sleep(interval)

# Example usage:
if __name__ == "__main__":
    fetch_and_log_data(room_id=101)
