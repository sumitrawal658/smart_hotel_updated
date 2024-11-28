from redis import Redis
import json
from datetime import datetime

class EventStream:
    def __init__(self):
        self.redis_client = Redis(host='localhost', port=6379, db=0)

    def publish_sensor_data(self, room_id, sensor_data):
        """Publish sensor data to Redis stream."""
        message = {
            'room_id': room_id,
            'data': sensor_data,
            'timestamp': datetime.utcnow().isoformat()
        }
        self.redis_client.xadd(
            'sensor_stream', 
            {'message': json.dumps(message)}
        )

    def get_latest_events(self, count=10):
        """Get latest events from the stream."""
        events = self.redis_client.xrevrange('sensor_stream', count=count)
        return [json.loads(event[1][b'message'].decode()) for event in events]

# Create a global event stream instance
event_stream = EventStream() 