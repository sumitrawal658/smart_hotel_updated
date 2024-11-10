from datetime import datetime, timedelta
from app import db
from app.models import SensorLog
from sqlalchemy import func

import logging

logging.basicConfig(
    filename='app.log',    # Log file name
    level=logging.INFO,     # Set the minimum log level to capture
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def log_alert(room_id, message):
    logging.info(f"{datetime.now()}: Alert in Room {room_id} - {message}")


def calculate_weekly_summary():
    one_week_ago = datetime.now() - timedelta(days=7)
    
    # Query each room's average CO2 and temperature over the last week
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
    
    # You could save these results to a `weekly_summaries` table if you want to persist them.

ALERT_THRESHOLD_CO2 = 1000  # Example threshold for CO2 in ppm
ALERT_THRESHOLD_TEMP = 30   # Example threshold for temperature in Celsius

def check_for_alerts():
    latest_logs = db.session.query(SensorLog) \
        .order_by(SensorLog.timestamp.desc()) \
        .limit(10) \
        .all()  # Adjust limit based on expected logs or frequency of check

    for log in latest_logs:
        co2_level = log.data['iaq']['co2']
        temperature = log.data['iaq']['temperature']

        if co2_level > ALERT_THRESHOLD_CO2:
            log_alert(log.room_id, f"CO2 level exceeded threshold: {co2_level} ppm")

            # Optional: Send an email, SMS, or log to alert service

        if temperature > ALERT_THRESHOLD_TEMP:
            log_alert(log.room_id, f"Temperature exceeded threshold: {temperature}°C")

            # Optional: Send an email, SMS, or log to alert service
