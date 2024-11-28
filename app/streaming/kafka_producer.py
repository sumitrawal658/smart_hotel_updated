from kafka import KafkaProducer
import json

class SensorDataProducer:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=['localhost:9092'],
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )
        
    def publish_sensor_data(self, room_id, sensor_data):
        self.producer.send(
            'sensor_data',
            key=str(room_id).encode(),
            value=sensor_data
        ) 