from redis import Redis
import json
import time
from .agents.data_logger import DataLoggerAgent
from .agents.occupancy_detector import OccupancyDetector
from flask import current_app

def process_stream_data(app):
    redis_client = Redis(host='localhost', port=6379, db=0)
    last_id = '0-0'

    # Initialize agents
    data_logger = DataLoggerAgent()
    occupancy_detector = OccupancyDetector()

    while True:
        try:
            # Read new messages from stream
            streams = redis_client.xread(
                {'sensor_stream': last_id}, 
                count=100,
                block=1000
            )

            if streams:
                for stream_name, messages in streams:
                    for message_id, data in messages:
                        # Process message
                        message = json.loads(data[b'message'].decode())
                        
                        # Process with Data Logger
                        data_logger.process_message(message)
                        
                        # Process with Occupancy Detector
                        occupancy_result = occupancy_detector.process_message(message)
                        if occupancy_result:
                            # Publish occupancy status to a different stream
                            redis_client.xadd(
                                'occupancy_stream',
                                {'message': json.dumps(occupancy_result)}
                            )
                        
                        last_id = message_id

        except Exception as e:
            print(f"Error processing stream: {e}")
            time.sleep(1)

if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        process_stream_data(app) 