from flask_apscheduler import APScheduler
from datetime import datetime
from app import create_app
from analytics import calculate_weekly_summary, check_for_alerts  # Import your functions
import logging
import atexit
from interface import iface  # Import the Gradio interface

logging.basicConfig(
    filename='app.log',    # Log file name
    level=logging.INFO,     # Set the minimum log level to capture
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
# Configuration for APScheduler
from pytz import utc

class Config:
    SCHEDULER_API_ENABLED = True

    SCHEDULER_TIMEZONE = utc


# Initialize the app and scheduler
app = create_app()
app.config.from_object(Config())
scheduler = APScheduler()
scheduler.init_app(app)

# Schedule the weekly summary job
scheduler.add_job(
    id='Weekly_Summary', 
    func=calculate_weekly_summary, 
    trigger='interval', 
    weeks=1, 
    next_run_time=datetime.now()
)

# Schedule the real-time alert job
scheduler.add_job(
    id='Real_Time_Alerts', 
    func=check_for_alerts, 
    trigger='interval', 
    minutes=10, 
    next_run_time=datetime.now()
)

# Start the scheduler
scheduler.start()

atexit.register(lambda: scheduler.shutdown())

def run_flask():
    app.run(debug=True)

def run_gradio():
    iface.launch()



if __name__ == "__main__":
    app.run(debug=True)
    iface.launch()  # This will open the Gradio UI in a new browser tab

