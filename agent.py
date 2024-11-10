from app import create_app, db
from app.models import SensorLog
import time
import requests
import logging

logging.basicConfig(
    filename='app.log',    # Log file name
    level=logging.INFO,     # Set the minimum log level to capture
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

app = create_app()
app.app_context().push()  # Set up the app context for database access

def fetch_and_log_data(room_id, interval=5):
    """Fetch data from the IoT simulation endpoint, adjust based on occupancy, and log it to the database."""
    url = f'http://127.0.0.1:5000/simulate/{room_id}'
    while True:
        try:
            response = requests.get(url)
            data = response.json()
            
            # Check presence state to adjust sensor data
            if data['life_being']['presence_state'] == 'absent':
                # Adjust the IAQ sensor data when room is empty
                data['iaq']['temperature'] = 18  # Lower the temperature
                data['iaq']['illuminance'] = 50  # Dim the lights
                data['iaq']['noise'] = 20  # Reduce noise level
                data['iaq']['humidity'] = 35.0  # Maintain humidity at a lower level
                # Optionally, set other parameters as "inactive" to simulate reduced usage

            # Log data to the database
            new_log = SensorLog(
                room_id=room_id,
                sensor_type="aggregate",  # Example sensor type
                data=data
            )
            db.session.add(new_log)
            db.session.commit()
            print(f"Logged data for room {room_id}: {data}")
        except Exception as e:
            print(f"Error fetching or logging data for room {room_id}: {e}")
        time.sleep(interval)

# Example usage:
if __name__ == "__main__":
    fetch_and_log_data(room_id=101)
